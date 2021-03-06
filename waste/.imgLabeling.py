def imgLabeling1(img1, img2, img3, img4, xoffsetL, xoffsetR):
    minlocL = np.argmin(np.sum(np.square(img1.astype(
        np.float64) - img2.astype(np.float64)), axis=2), axis=1)
    minlocR = np.argmin(np.sum(np.square(img3.astype(
        np.float64) - img4.astype(np.float64)), axis=2), axis=1)
    minlocL = minlocL + xoffsetL
    minlocR = minlocR + xoffsetR
    mask = np.ones((1280, 2560, 3), np.float64)
    for i in range(1280):
        mask[i, minlocL[i]:minlocR[i]] = 0
        mask[i, minlocL[i]] = 0.5
        mask[i, minlocR[i]] = 0.5
    return mask


def imgLabeling2(img1, img2, img3, img4, maskSize, xoffsetL, xoffsetR):
    if len(img1.shape) == 3:
        errL = np.sum(np.square(img1.astype(np.float64) -
                                img2.astype(np.float64)), axis=2)
        errR = np.sum(np.square(img3.astype(np.float64) -
                                img4.astype(np.float64)), axis=2)
    else:
        errL = np.square(img1.astype(np.float64) - img2.astype(np.float64))
        errR = np.square(img3.astype(np.float64) - img4.astype(np.float64))
    EL = np.zeros(errL.shape, np.float64)
    ER = np.zeros(errR.shape, np.float64)
    EL[0] = errL[0]
    ER[0] = errR[0]
    for i in range(1, maskSize[1]):
        EL[i, 0] = errL[i, 0] + min(EL[i - 1, 0], EL[i - 1, 1])
        ER[i, 0] = errR[i, 0] + min(ER[i - 1, 0], ER[i - 1, 1])
        for j in range(1, EL.shape[1] - 1):
            EL[i, j] = errL[i, j] + \
                min(EL[i - 1, j - 1], EL[i - 1, j], EL[i - 1, j + 1])
            ER[i, j] = errR[i, j] + \
                min(ER[i - 1, j - 1], ER[i - 1, j], ER[i - 1, j + 1])
        EL[i, -1] = errL[i, -1] + min(EL[i - 1, -1], EL[i - 1, -2])
        ER[i, -1] = errR[i, -1] + min(ER[i - 1, -1], ER[i - 1, -2])

    minlocL = np.argmin(EL, axis=1) + xoffsetL
    minlocR = np.argmin(ER, axis=1) + xoffsetR
    mask = np.ones((maskSize[1], maskSize[0], 3), np.float64)
    for i in range(maskSize[1]):
        mask[i, minlocL[i]:minlocR[i]] = 0
        mask[i, minlocL[i]] = 0.5
        mask[i, minlocR[i]] = 0.5
    return mask
