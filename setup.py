from setuptools import find_packages, setup


setup(
    name='qx-app-pay',
    version='1.0.0',
    author='Shawn',
    author_email='q-x64@live.com',
    url='https://github.com/qx-oo/qx-app-pay/',
    description='Django app pay.',
    long_description=open("README.md").read(),
    packages=find_packages(include=["qx_app_pay", "qx_vip"]),
    install_requires=[
        'requests>=2.24',
        'cryptography>=2.9',
        'djangorestframework >= 3.10',
    ],
    python_requires='>=3.8',
    platforms='any',
)
