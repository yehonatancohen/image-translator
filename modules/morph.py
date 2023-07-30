import numpy as np

def erode(image, kernel = np.ones((6, 6), 'uint8')):
    """
    Performs the erosion operation on a binary image using the specified kernel.

    Parameters:
        image (numpy.ndarray): The binary input image (0s and 1s).
        kernel (numpy.ndarray): The structuring element (binary matrix) used for erosion.

    Returns:
        numpy.ndarray: The eroded binary image.
    """
    h,w = image.shape
    result = np.zeros_like(image)
    padded_image = np.pad(image, (kernel.shape[0] // 2, kernel.shape[1] // 2), mode='constant')

    for i in range(h):
        for j in range(w):
            if np.all(padded_image[i:i+kernel.shape[0], j:j+kernel.shape[1]] * kernel):
                result[i, j] = 1

    return result

def dilate(image, kernel = np.ones((3, 3), dtype=np.uint8)):
    """
    Performs the dilation operation on a binary image using the specified kernel.

    Parameters:
        image (numpy.ndarray): The binary input image (0s and 1s).
        kernel (numpy.ndarray): The structuring element (binary matrix) used for dilation.

    Returns:
        numpy.ndarray: The dilated binary image.
    """
    result = np.zeros_like(image)
    padded_image = np.pad(image, (kernel.shape[0] // 2, kernel.shape[1] // 2), mode='constant')

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if np.any(padded_image[i:i+kernel.shape[0], j:j+kernel.shape[1]] * kernel):
                result[i, j] = 1

    return result

def closing(image, kernel):
    """
    Performs the closing operation on a binary image using the specified kernel.

    Parameters:
        image (numpy.ndarray): The binary input image (0s and 1s).
        kernel (numpy.ndarray): The structuring element (binary matrix) used for closing.

    Returns:
        numpy.ndarray: The result of the closing operation on the input image.
    """
    dilated_image = dilate(image, kernel)
    closed_image = erode(dilated_image, kernel)
    return closed_image

def opening(image, kernel):
    """
    Performs the opening operation on a binary image using the specified kernel.

    Parameters:
        image (numpy.ndarray): The binary input image (0s and 1s).
        kernel (numpy.ndarray): The structuring element (binary matrix) used for opening.

    Returns:
        numpy.ndarray: The result of the opening operation on the input image.
    """
    eroded_image = erode(image, kernel)
    opened_image = dilate(eroded_image, kernel)
    return opened_image

# Example usage:
if __name__ == "__main__":
    # Create a binary image (0s and 1s) for demonstration
    image = np.array([[0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0],
                      [0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0]], dtype=np.uint8)

    # Create a simple 3x3 square kernel
    kernel = np.ones((3, 3), dtype=np.uint8)

    # Apply erosion
    eroded_image = erode(image, kernel)
    print("Eroded Image:")
    print(eroded_image)

    # Apply dilation
    dilated_image = dilate(image, kernel)
    print("\nDilated Image:")
    print(dilated_image)
