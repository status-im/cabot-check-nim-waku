import subprocess
from os import path
from os import environ as env
from celery.utils.log import get_task_logger
from django.db.models import BooleanField, CharField, TextField

from cabot.cabotapp.models import StatusCheck, StatusCheckResult

log = get_task_logger(__name__)

RAW_DATA_TEMPLATE = '''
Command:
{}
Return Code:
{}
Stdout:
{}
Stderr:
{}
'''

class NimWakuException(Exception):
    def __init__(self, message, raw_data):
        self.message = message
        self.raw_data = raw_data

class NimWakuStatusCheck(StatusCheck):
    check_name = 'nim-waku'
    edit_url_name = 'update-nim-waku-check'
    duplicate_url_name = 'duplicate-nim-waku-check'
    icon_class = 'glyphicon-random'

    LOG_LEVELS = (
        ('TRACE', 'TRACE'),
        ('DEBUG', 'DEBUG'),
        ('INFO',  'INFO'),
        ('WARN',  'WARN'),
        ('ERROR', 'ERROR'),
    )

    log_level = CharField(
        max_length=10,
        choices=LOG_LEVELS,
        default='ERROR',
        help_text='Canary tool logging level.'
    )
    address = TextField(help_text='Waku node multiaddress.')
    proto_relay = BooleanField(default=True, help_text='Relay Protocol Check')
    proto_store = BooleanField(default=False, help_text='Store Protocol Check')
    proto_filter = BooleanField(default=False, help_text='Filter Protocol Check')
    proto_lightpush = BooleanField(default=False, help_text='Lightpush Protocol Check')

    def _run(self):
        result = StatusCheckResult(status_check=self)

        try:
            rval = self._check()
        except NimWakuException as e:
            result.raw_data = e.raw_data
            result.error = u'Error occurred: {}'.format(e.message)
            result.succeeded = False
        except Exception as e:
            result.error = u'Error occurred: {}'.format(e)
            result.succeeded = False
        else:
            result.raw_data = rval
            result.succeeded = True

        return result

    def _check(self):
        canary_path = env.get('NIM_WAKU_CANARY_PATH')
        if canary_path is None:
            raise Exception('NIM_WAKU_CANARY_PATH env variable not found!')

        if not path.exists(canary_path):
            raise Exception('No such file: {}'.format(canary_path))

        command = (
            [ canary_path,
             '--address={}'.format(self.address),
             '--timeout={}'.format(self.timeout-1),
             '--log-level={}'.format(self.log_level) ]
            + (['--protocol=relay'] if self.proto_relay else [])
            + (['--protocol=store'] if self.proto_store else [])
            + (['--protocol=filter'] if self.proto_filter else [])
            + (['--protocol=lightpush'] if self.proto_lightpush else [])
        )

        log.info('Checking: %s', self.name)

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        process.wait()
        return_code = process.poll()

        rval = RAW_DATA_TEMPLATE.format(
            ' \\\n  '.join(command), return_code, stdout, stderr
        )

        log.debug('stdout: %s', stdout)
        log.debug('stderr: %s', stderr)

        if return_code != 0:
            raise NimWakuException('Failed: {}'.format(stderr), rval)

        return rval
