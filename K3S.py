import K3S

config = K3S.Config()

print(config.LOG_LOCATION)

logger = K3S.Log()
logger.debug('append')

