import numpy as np
import matplotlib.pyplot as plt

with open('input.txt') as file:
    image = [int(x) for x in file.readline().strip()]

xy = (6, 25)
z = int(len(image) / (xy[0] * xy[1]))
shape = (z,) + xy

image_np = np.reshape(image, shape).astype(np.ubyte)

# part 1
layer_nonzero_min = np.argmin(np.sum(image_np == 0, axis=(1, 2)))
image_nonzero_min = image_np[layer_nonzero_min, :, :]
print(np.sum(image_nonzero_min == 1) * np.sum(image_nonzero_min == 2))

# part 2
final_image = np.full(xy, 2, dtype=np.ubyte)
for layer in range(z):
    final_image = np.where(final_image == 2, image_np[layer, :, :], final_image)

plt.imshow(final_image, interpolation='none')
plt.savefig('output.png')
plt.show()
plt.close()
# CEKUA
