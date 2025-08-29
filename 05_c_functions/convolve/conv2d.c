// conv2d.c
#include <stddef.h>

static inline float clamp_read(const float *img, int H, int W, int r, int c) {
    // zero-padding (used by SAME)
    if (r < 0 || r >= H || c < 0 || c >= W) return 0.0f;
    return img[(size_t)r * (size_t)W + (size_t)c];
}

void conv2d_valid_f32(
    const float *img, int H, int W,
    const float *ker, int KH, int KW,
    float *out // size: (H-KH+1) * (W-KW+1)
) {
    int OH = H - KH + 1;
    int OW = W - KW + 1;
    for (int r = 0; r < OH; ++r) {
        for (int c = 0; c < OW; ++c) {
            float acc = 0.0f;
            for (int kr = 0; kr < KH; ++kr) {
                const int ir = r + kr;
                const float *img_row = img + (size_t)ir * (size_t)W + (size_t)c;
                const float *ker_row = ker + (size_t)kr * (size_t)KW;
                for (int kc = 0; kc < KW; ++kc) {
                    acc += img_row[kc] * ker_row[kc];
                }
            }
            out[(size_t)r * (size_t)OW + (size_t)c] = acc;
        }
    }
}

void conv2d_same_f32(
    const float *img, int H, int W,
    const float *ker, int KH, int KW,
    float *out // size: H * W
) {
    int krc = KH / 2; // kernel row center (assumes odd KH, KW)
    int kcc = KW / 2;
    for (int r = 0; r < H; ++r) {
        for (int c = 0; c < W; ++c) {
            float acc = 0.0f;
            for (int kr = 0; kr < KH; ++kr) {
                int ir = r + (kr - krc);
                for (int kc = 0; kc < KW; ++kc) {
                    int ic = c + (kc - kcc);
                    float v = clamp_read(img, H, W, ir, ic);
                    float k = ker[(size_t)kr * (size_t)KW + (size_t)kc];
                    acc += v * k;
                }
            }
            out[(size_t)r * (size_t)W + (size_t)c] = acc;
        }
    }
}
