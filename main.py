from PIL import Image, ImageDraw, ImageOps
from uuid import uuid4
from random import getrandbits, randint

class Avatar_Generator():
	"""
	Class representing an avatar generator.

	Attributes:
	- width (int): width of the avatar in pixels
	- first_half (PIL.Image.Image): the first half of the avatar image
	- final_image (PIL.Image.Image): the final generated avatar image
	- background_color (tuple[int]): the RGB value of the background color, default is randomly generated
	- square_color (tuple[int]): the RGB value of the color for the random squares, default is a lighter version of the background color
	
	Methods:
	- __init__(self, width, background_color=None, square_color=None):
		Initializes the avatar generator with the given width and background/square colors.

	- Make_RGB_Lighter(self):
		Function to create a lighter version of the background color for the random squares.

	- Create_First_Half(self):
		Creates the first half of the avatar image with the background color.

	- Draw_Random_Squares(self):
		Draws random squares on the first half of the avatar image with the square color.

	- Expand_Image(self, width=None):
		Expands the final avatar image with the given width and background color.

	- Get_Result(self, directory='.', save=True, show=False):
		Returns the final avatar image and optionally saves it to a directory and/or shows it on screen.
	"""

	def __init__(self, width, background_color=None, square_color=None):
		"""
		Initialize the Avatar_Generator class with the given width for avatar, 
		and the optional background and square colors.
		
		Args:
			width (int): The width and height (if width = 1000 then height is also 1000 because it's square) of the generated image.
			background_color (tuple, optional): The RGB tuple for the background color. 
				If not given, a random RGB tuple will be generated.
			square_color (tuple, optional): The RGB tuple for the square color. 
				If not given, a lighter version of the background color will be used.
		"""
		
		self.width = width
		self.first_half = None
		self.final_image = None

		self.background_color = tuple((randint(0, 255 + 1) for _ in range(3))) if not background_color else background_color
		self.square_color = self.Make_RGB_Lighter() if not square_color else square_color

	def Make_RGB_Lighter(self) -> tuple:
		"""
		Function to create a lighter version of the background color for the random squares.

		Returns:
		- tuple[int]: the RGB value of the lighter color
		"""

		self.square_color = []
		for value in self.background_color:
			new_value = value + 50
			if new_value <= 255:
				self.square_color.append(new_value)
			else:
				self.square_color.append(255)

		return tuple(self.square_color)

	def Create_First_Half(self) -> Image:
		"""
		Creates the first half of the avatar image with the background color.

		Returns:
		- PIL.Image.Image: the first half of the avatar image
		"""

		self.first_half = Image.new(mode='RGB', size=(round(self.width / 2), self.width), color=self.background_color)
		return self.first_half

	def Draw_Random_Squares(self) -> None:
		"""
		Draws random squares on the first half of the avatar image with the square color.
		"""

		max_square_size = round((self.width / 2) / 3)

		draw = ImageDraw.Draw(self.first_half)

		for y in range(5):
			for x in range(3):
				if bool(getrandbits(1)):
					draw.rectangle(
						[
							(max_square_size * x, max_square_size * y),
							(max_square_size * x + max_square_size, max_square_size * y + max_square_size)
						],
						fill=self.square_color
					)

		mirror = ImageOps.mirror(self.first_half)
		self.final_image = Image.new(mode='RGB', size=(self.width , self.width))
		self.final_image.paste(self.first_half, (0, 0))
		self.final_image.paste(mirror, (self.first_half.size[0], 0))

	def Expand_Image(self, width=None) -> None:
		"""
		Expands the final avatar image with the given width and background color.

		Arguments:
		- width (int): the width of the border to add to the final image
		"""

		if not width:
			width = int((self.width * 125) / 1000)

		self.final_image = ImageOps.expand(self.final_image, border=width, fill=self.background_color)

	def Get_Result(self, directory='.', save=True, show=False) -> Image:
		"""
		Returns the final avatar image and optionally saves it to a directory and/or shows it on screen.

		Arguments:
		- directory (str): the directory to save the image in
		- save (bool): whether or not to save the image
		- show (bool): whether or not to show the image on screen

		Returns:
		- PIL.Image.Image: the final generated avatar image
		"""

		if show: self.final_image.show()
		if save:
			self.final_image.save(f'{directory}/generation-{uuid4()}.jpg', 'jpeg')
		return self.final_image

if __name__ == '__main__':
	ag = Avatar_Generator(width=1000)
	ag.Create_First_Half()
	ag.Draw_Random_Squares()
	ag.Expand_Image()
	ag.Get_Result(directory='generations', show=True)