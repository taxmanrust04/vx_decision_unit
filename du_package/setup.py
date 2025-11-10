from setuptools import setup, find_packages

package_name = 'decision_unit'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Parth Pahinkar',
    maintainer_email='parth.pahinkar@hs-coburg.de',
    description='Decision Unit implemented.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'decision_core_fsm = decision_unit.decision_core_fsm:main',
        ],
    },
)

