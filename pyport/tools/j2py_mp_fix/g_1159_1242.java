                while (g.cL < 3) {
                    if (g.dU[g.dW] == g.cL) {
                    this.a(g.e, l.eW[g.cL], g.cW - 28, g.cX - 15 + g.cL * 19, 1, 0xFFFFFF);
                    switch (g.cL) {
                        case 0: {
                            this.a(g.e, l.eW[3 + g.an], g.cW + 33, g.cX - 15, 1, 0xFFFFFF);
                            break;
                        }
                        case 1: {
                            this.a(g.e, l.eW[8 + g.ap], g.cW + 33, g.cX - 15 + g.cL * 19, 1, 0xFFFFFF);
                            break;
                        }
                        case 2: {
                            if (g.ah() > 0) {
                                int var2_11 = 0;
                                while (var2_11 < g.ah()) {
                                    f.b(g.e, g.cW + 21 + 5 * var2_11, g.cX - 13 + g.cL * 19, 3, 8, 0xFFFFFF);
                                    ++var2_11;
                                }
                                break;
                            }
                            this.a(g.e, l.eW[6 + (g.ah() > 0 ? 0 : 1)], g.cW + 33, g.cX - 15 + g.cL * 19, 1, 0xFFFFFF);
                        }
                    }
                    this.c(g.e, g.cW - 58, g.cX - 16 + g.cL * 19, 61, 14, 3);
                    this.c(g.e, g.cW + 13, g.cX - 16 + g.cL * 19, 39, 14, 3);
                    if (g.da % 4 < 2) {
                        g.c(g.cW + 6, g.cX - 13 + g.cL * 19, g.di[1]);
                        g.b(g.cW + 59, g.cX - 13 + g.cL * 19, g.di[1]);
                    }
                    } else {
                    switch (g.cL) {
                        case 0: {
                            this.a(g.e, l.eW[3 + g.an], g.cW + 33, g.cX - 15, 1, 0x646464);
                            break;
                        }
                        case 1: {
                            this.a(g.e, l.eW[8 + g.ap], g.cW + 33, g.cX - 15 + g.cL * 19, 1, 0x646464);
                            break;
                        }
                        case 2: {
                            if (g.ah() > 0) {
                                int var2_11 = 0;
                                while (var2_11 < g.ah()) {
                                    f.b(g.e, g.cW + 21 + 5 * var2_11, g.cX - 13 + g.cL * 19, 3, 8, 0x646464);
                                    ++var2_11;
                                }
                                break;
                            }
                            this.a(g.e, l.eW[6 + (g.ah() > 0 ? 0 : 1)], g.cW + 33, g.cX - 15 + g.cL * 19, 1, 0x646464);
                        }
                    }
                    }
                    ++g.cL;
                }
