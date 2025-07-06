import pygame

def resize_image(input_path, output_path, size):
    """
    Resizes an image to the specified size.

    Args:
        input_path (str): Path to the input image.
        output_path (str): Path to save the resized image.
        size (tuple): A tuple (width, height) for the new size.
    """
    pygame.init()
    try:
        image = pygame.image.load(input_path)
        resized_image = pygame.transform.scale(image, size)
        pygame.image.save(resized_image, output_path)
        print(f"Image saved to {output_path}")
    except pygame.error as e:
        print(f"Error processing image: {e}")
    finally:
        pygame.quit()

if __name__ == '__main__':
    # Path to your original image
    input_image_path = '/home/mdiloreto/vscode/pygame/recursos/imagenes/fondo2.png'
    # Path to save the new resized image
    output_image_path = '/home/mdiloreto/vscode/pygame/recursos/imagenes/fondo2_resized.png'
    # New dimensions
    new_size = (1280, 720)

    resize_image(input_image_path, output_image_path, new_size)
