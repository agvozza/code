/* Exact Banker / Player / Tie probabilities for the next hand dealt from a
 * shoe with counts[v] cards of each baccarat value v (0-9). Same enumeration
 * as baccarat/counting.py: unordered two-card hands, then the drawing rules. */

static int banker_draws(int bt, int p3) {  /* p3 < 0: Player stood */
    if (p3 < 0) return bt <= 5;
    if (bt <= 2) return 1;
    if (bt == 3) return p3 != 8;
    if (bt == 4) return p3 >= 2 && p3 <= 7;
    if (bt == 5) return p3 >= 4 && p3 <= 7;
    if (bt == 6) return p3 == 6 || p3 == 7;
    return 0;
}

static void settle(int p, int b, double w, double *pb, double *pp, double *pt) {
    if (b > p) *pb += w; else if (p > b) *pp += w; else *pt += w;
}

void probabilities(const int *counts, double *out) {
    int c[10];
    long n = 0;
    for (int v = 0; v < 10; v++) { c[v] = counts[v]; n += c[v]; }
    double pb = 0, pp = 0, pt = 0;
    for (int a = 0; a < 10; a++) for (int b = a; b < 10; b++) {
        double wa = c[a]; c[a]--;
        double wb = c[b]; c[b]--;
        if (wa > 0 && wb > 0) {
            double wpl = wa * wb * (a == b ? 1 : 2);
            int ptot = (a + b) % 10;
            for (int x = 0; x < 10; x++) for (int y = x; y < 10; y++) {
                double wx = c[x]; c[x]--;
                double wy = c[y]; c[y]--;
                if (wx > 0 && wy > 0) {
                    double w = wpl * wx * wy * (x == y ? 1 : 2);
                    int btot = (x + y) % 10;
                    double m = (double)(n - 4);
                    if (ptot >= 8 || btot >= 8) {
                        settle(ptot, btot, w, &pb, &pp, &pt);
                    } else if (ptot >= 6) {  /* Player stands */
                        if (banker_draws(btot, -1)) {
                            for (int v = 0; v < 10; v++) if (c[v] > 0)
                                settle(ptot, (btot + v) % 10, w * c[v] / m, &pb, &pp, &pt);
                        } else settle(ptot, btot, w, &pb, &pp, &pt);
                    } else {
                        for (int p3 = 0; p3 < 10; p3++) {
                            if (c[p3] <= 0) continue;
                            double q = w * c[p3] / m;
                            int pt3 = (ptot + p3) % 10;
                            if (banker_draws(btot, p3)) {
                                c[p3]--;
                                for (int v = 0; v < 10; v++) if (c[v] > 0)
                                    settle(pt3, (btot + v) % 10, q * c[v] / (m - 1), &pb, &pp, &pt);
                                c[p3]++;
                            } else settle(pt3, btot, q, &pb, &pp, &pt);
                        }
                    }
                }
                c[x]++; c[y]++;
            }
        }
        c[a]++; c[b]++;
    }
    double total = pb + pp + pt;
    out[0] = pb / total; out[1] = pp / total; out[2] = pt / total;
}
