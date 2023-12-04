##########################################################################
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################

from distutils.core import setup
from glob import glob
setup(name='MathsTutor',
      version='1.0',
      description='Game for learning mathematical operations',
      author='Roopasree AP',
      author_email='roopasreeap@gmail.com',
      url='https://github.com/roopasreeap/Maths-Tutor',
      license = 'GPL-3',
      packages=['MathsTutor'],
      data_files=[('share/maths-tutor/',['icon.png', 'data.txt']),

      ('share/maths-tutor/images/',['images/excellent-1.gif']),
      ('share/maths-tutor/images/',['images/excellent-2.gif']),
      ('share/maths-tutor/images/',['images/excellent-3.gif']),
      ('share/maths-tutor/images/',['images/finished-1.gif']),
      ('share/maths-tutor/images/',['images/finished-2.gif']),
      ('share/maths-tutor/images/',['images/finished-3.gif']),
      ('share/maths-tutor/images/',['images/good-1.gif']),
      ('share/maths-tutor/images/',['images/good-2.gif']),
      ('share/maths-tutor/images/',['images/good-3.gif']),
      ('share/maths-tutor/images/',['images/not-bad-1.gif']),
      ('share/maths-tutor/images/',['images/not-bad-2.gif']),
      ('share/maths-tutor/images/',['images/not-bad-3.gif']),
      ('share/maths-tutor/images/',['images/okay-1.gif']),
      ('share/maths-tutor/images/',['images/okay-2.gif']),
      ('share/maths-tutor/images/',['images/okay-3.gif']),
      ('share/maths-tutor/images/',['images/question-1.gif']),
      ('share/maths-tutor/images/',['images/question-2.gif']),
      ('share/maths-tutor/images/',['images/very-good-1.gif']),
      ('share/maths-tutor/images/',['images/very-good-2.gif']),
      ('share/maths-tutor/images/',['images/very-good-3.gif']),
      ('share/maths-tutor/images/',['images/welcome-1.gif']),
      ('share/maths-tutor/images/',['images/welcome-2.gif']),
      ('share/maths-tutor/images/',['images/welcome-3.gif']),
      ('share/maths-tutor/images/',['images/wrong-anwser-1.gif']),
      ('share/maths-tutor/images/',['images/wrong-anwser-2.gif']),
      ('share/maths-tutor/images/',['images/wrong-anwser-3.gif']),
      ('share/maths-tutor/images/',['images/wrong-anwser-repeted-1.gif']),
      ('share/maths-tutor/images/',['images/wrong-anwser-repeted-2.gif']),

      ('share/maths-tutor/sounds/',['sounds/backgroundmusic.ogg']),
      ('share/maths-tutor/sounds/',['sounds/coin.ogg']),
      ('share/maths-tutor/sounds/',['sounds/excellent-1.ogg']),
      ('share/maths-tutor/sounds/',['sounds/excellent-2.ogg']),
      ('share/maths-tutor/sounds/',['sounds/excellent-3.ogg']),
      ('share/maths-tutor/sounds/',['sounds/finished-1.ogg']),
      ('share/maths-tutor/sounds/',['sounds/finished-2.ogg']),
      ('share/maths-tutor/sounds/',['sounds/finished-3.ogg']),
      ('share/maths-tutor/sounds/',['sounds/good-1.ogg']),
      ('share/maths-tutor/sounds/',['sounds/good-2.ogg']),
      ('share/maths-tutor/sounds/',['sounds/good-3.ogg']),
      ('share/maths-tutor/sounds/',['sounds/not-bad-1.ogg']),
      ('share/maths-tutor/sounds/',['sounds/not-bad-2.ogg']),
      ('share/maths-tutor/sounds/',['sounds/not-bad-3.ogg']),
      ('share/maths-tutor/sounds/',['sounds/okay-1.ogg']),
      ('share/maths-tutor/sounds/',['sounds/okay-2.ogg']),
      ('share/maths-tutor/sounds/',['sounds/okay-3.ogg']),
      ('share/maths-tutor/sounds/',['sounds/question.ogg']),
      ('share/maths-tutor/sounds/',['sounds/very-good-1.ogg']),
      ('share/maths-tutor/sounds/',['sounds/very-good-2.ogg']),
      ('share/maths-tutor/sounds/',['sounds/very-good-3.ogg']),
      ('share/maths-tutor/sounds/',['sounds/welcome.ogg']),
      ('share/maths-tutor/sounds/',['sounds/wrong-anwser-1.ogg']),
      ('share/maths-tutor/sounds/',['sounds/wrong-anwser-2.ogg']),
      ('share/maths-tutor/sounds/',['sounds/wrong-anwser-3.ogg']),
      ('share/maths-tutor/sounds/',['sounds/wrong-anwser-repeted-1.ogg']),
      ('share/maths-tutor/sounds/',['sounds/wrong-anwser-repeted-2.ogg']),
      ('share/maths-tutor/sounds/',['sounds/wrong-anwser-repeted-3.ogg']),

      ('share/applications/',['maths-tutor.desktop']),
      ('bin/',['maths-tutor'])]
      )
# sudo python3 setup.py install --install-data=/usr
