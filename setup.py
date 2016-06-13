from setuptools import setup


setup(
    name="btrfstm",
    version="0.1.0",
    description="A tool to manage Timed BTRFS Snapshots",
    author="Max Huang",
    author_email="maxh1981@gmail.com",
    license="MIT",
    packages=[
        "btrfstm"],
    install_requires=[
        "sh"],
    entry_points={
        "console_scripts":[
            "btrfstm=btrfstm.cli:main"]}
)
