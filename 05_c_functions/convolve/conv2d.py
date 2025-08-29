import os, time, ctypes as ct
import numpy as np
from numpy.ctypeslib import ndpointer
from PIL import Image

# load shared library
libname = "./libconv2d.so" if os.name != "nt" else "./conv2d.dll"
lib = ct.CDLL(os.path.abspath(libname))

# declare signatures
f32p = ndpointer(dtype=np.float32, ndim=1, flags="C_CONTIGUOUS")

lib.conv2d_valid_f32.argtypes = [f32p, ct.c_int, ct.c_int, f32p, ct.c_int, ct.c_int, f32p]
lib.conv2d_valid_f32.restype  = None

lib.conv2d_same_f32.argtypes  = [f32p, ct.c_int, ct.c_int, f32p, ct.c_int, ct.c_int, f32p]
lib.conv2d_same_f32.restype   = None

# naive pure-Python baseline (triple loop) — intentionally slow
def conv2d_valid_py(img, ker):
    H, W = len(img), len(img[0])
    KH, KW = len(ker), len(ker[0])
    OH, OW = H - KH + 1, W - KW + 1
    out = [[0.0]*OW for _ in range(OH)]
    for r in range(OH):
        for c in range(OW):
            acc = 0.0
            for kr in range(KH):
                for kc in range(KW):
                    acc += img[r+kr][c+kc] * ker[kr][kc]
            out[r][c] = acc
    return out

# helpers to call C
def conv2d_valid_c(img: np.ndarray, ker: np.ndarray) -> np.ndarray:
    assert img.dtype == np.float32 and ker.dtype == np.float32
    H, W  = img.shape
    KH, KW = ker.shape
    OH, OW = H - KH + 1, W - KW + 1
    out = np.empty((OH, OW), dtype=np.float32)
    lib.conv2d_valid_f32(img.ravel(), H, W, ker.ravel(), KH, KW, out.ravel())
    return out

def conv2d_same_c(img: np.ndarray, ker: np.ndarray) -> np.ndarray:
    assert img.dtype == np.float32 and ker.dtype == np.float32
    H, W  = img.shape
    KH, KW = ker.shape
    out = np.empty((H, W), dtype=np.float32)
    lib.conv2d_same_f32(img.ravel(), H, W, ker.ravel(), KH, KW, out.ravel())
    return out

        
def define_kernel(size=3, kernel_type="gaussian", custom=None):
    """
    Generate a normalized kernel.
    size: odd integer (e.g., 3, 5, 7)
    kernel_type: "gaussian", "box", or "custom"
    custom: a numpy array for custom kernel
    """
    if kernel_type == "custom" and custom is not None:
        ker_np = np.array(custom, dtype=np.float32)
        ker_np /= ker_np.sum()
        return ker_np

    if kernel_type == "box":
        ker_np = np.ones((size, size), dtype=np.float32)
        ker_np /= ker_np.sum()
        return ker_np

    if kernel_type == "gaussian":
        # Create a 2D Gaussian kernel
        sigma = size / 6.0  # heuristic: covers most of the kernel
        ax = np.linspace(-(size // 2), size // 2, size)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
        ker_np = kernel.astype(np.float32)
        ker_np /= ker_np.sum()
        return ker_np

    # Default: 3x3 box
    ker_np = np.ones((3, 3), dtype=np.float32)
    ker_np /= ker_np.sum()
    return ker_np

def load_image(fname):
    # Load image and convert to grayscale
    img_pil = Image.open(fname).convert("L")  # "L" mode is grayscale

    # Convert to numpy array and float32
    img_np = np.array(img_pil, dtype=np.float32)

    # Optionally normalize (0-1)
    img_np /= 255.0
    return img_np

def arg_parse():
    import argparse
    parser = argparse.ArgumentParser(description="2D Convolution using C extension")
    parser.add_argument("--image", type=str, default="lena_gray.gif", help="Path to input image")
    parser.add_argument("--kernel_size", type=int, default=7, help="Size of the kernel (odd integer)")
    parser.add_argument("--kernel_type", type=str, choices=["gaussian", "box", "custom"], default="gaussian", help="Type of kernel")
    args = parser.parse_args()
    return args

def main():
    args = arg_parse()
    img_np = load_image(args.image)
    ker_np = define_kernel(args.kernel_size)

    # --- timing: Python (tiny problem) vs C (big problem) ---
    # Python baseline would be unbearably slow at 1024², so time it on smaller data
    img_py = [[float(x) for x in row] for row in img_np[:, :]]
    print("shape:", img_np.shape)

    t0 = time.perf_counter()
    _ = conv2d_valid_py(img_py, ker_np)
    t1 = time.perf_counter()

    t2 = time.perf_counter()
    out_np = conv2d_valid_c(img_np, ker_np)
    t3 = time.perf_counter()
    # Convert result back to image and save
    out_img = Image.fromarray(np.clip(out_np * 255, 0, 255).astype(np.uint8))
    out_img.save("convolved_image.jpg")

    print(f"Pure Python ({img_np.shape} ⊗ {ker_np.shape}): {t1 - t0:.3f} s")
    print(f"C via ctypes ({img_np.shape} ⊗ {ker_np.shape}): {t3 - t2:.3f} s")

main()