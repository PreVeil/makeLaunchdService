from distutils.core import setup
setup(name='makeLaunchdService',
      version='1.0',
      packages=['makeLaunchdService'],
      package_data={'makeLaunchdService' : ['launchd.template.plist']},
)
