from setuptools import setup


APP_NAME, APP_SLUG = 'ThemeToggler', 'themetoggler'

setup(
    name=APP_NAME,
    py_modules=[APP_SLUG],
    version='1.1.0',
    install_requires=[],
    entry_points=f'''
        [console_scripts]
        {APP_SLUG}={APP_SLUG}:main
    ''',
)
