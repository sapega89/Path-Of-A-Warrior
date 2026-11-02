                g.bB = 99;
                if (g.cs == -1) {
                    g.bB = 2;
                } else if (g.cs == -3) {
                    g.bB = 1;
                } else if (g.cs == -4) {
                    g.bB = 0;
                } else if (g.cs == -2) {
                    if (g.bD > 0) {
                        g.cN = 0;
                        while (g.cN < g.bD) {
                            if (g.bX[0] >= g.cI[g.bE[g.cN] - 3]) {
                                g.bB = 20;
                                break;
                            }
                            ++g.cN;
                        }
                    }
                } else if (g.cs == -7 && !g.G) {
                    g.G = true;
                    g.D = true;
                    g.E = 1;
                    g.F = System.currentTimeMillis();
                }
