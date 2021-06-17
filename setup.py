from distutils.core import setup

setup(
  name = 'Broccoli',         # How you named your package folder (MyLib)
  packages = ['Broccoli'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='gpl-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Lightweight Asynchronius Web framework based on japronto styled like flask',   # Give a short description about your library
  author = 'brosskev',                   # Type in your name
  author_email = 'jecob.akhmedov@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Jacobamv/Broccoli',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Jacobamv/Broccoli/archive/refs/tags/v_01.tar.gz',    # I explain this later on
  keywords = ['Web', 'Framework', 'Python', "Flask", "Asynchronius", "Fast", "japronto"],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'japronto',
          'jinja2',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',   # Again, pick a license
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9"
  ],
)
