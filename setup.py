from setuptools import setup, find_packages

setup(
    name="menace-tictactoe",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'menace-train = examples.train_and_plot:main',
            'menace-play = examples.play_vs_human:main',
        ],
    },
)
