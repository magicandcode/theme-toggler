from setuptools import setup


APP_NAME, APP_SLUG = 'ThemeToggler', 'theme_toggler'

setup(
    name=APP_NAME,
    py_modules=[APP_SLUG],
    install_requires=[],
    entry_points=f'''
        [console_scripts]
        {APP_SLUG}={APP_SLUG}:main
    ''',
)
