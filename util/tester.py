from multiprocessing import Process, Queue
import os

import numpy as np

a = 10
b = 1337
Q = Queue()

def adder(name: str, c: int):
    c + 1

# def mp_calc(self, g_calc, z_calc, U_calc, e_kons):
#         gbar = g_calc + z_calc * U_calc
#         Rbar = self.compute_R(gbar)
#         ebar = np.sum(np.square(Rbar))
#         zeta = z_calc * 0.7
#         if ebar < e_kons or np.abs(ebar - e_kons) < self.tol:
#             self.cancel = 1
#         return gbar, Rbar, ebar

#
# processes = []
#
# if __name__ == "__main__":
#     print(__name__)
#     for i in range(os.cpu_count()):
#         print('registering proccess %d' % i)
#         processes.append(Process(target=adder("thread" + str(i), b)))
#
#     for process in processes:
#         process.daba = 10
#         process.start()

    # print(Q.get())
    #
    # for process in processes:
    #     process.join

    # print(Q.get())
    # print (type(Q.get()))

print("done")


# TODO: when ebar fulfills condition,
#  kill all processes and take the process with highest ebar
#  maybe get dict with all ebars -> search for highest value?
#  like ebar_dict = {1: ebar1, 2:ebar2,... 7: ebar7}
# while ((k < self.N) and (e > self.tol)):
#     print("k = " + str(k))
#     zeta = self.zeta
#     while zeta > 10 - 12:
#         print("zeta = ", zeta, "  e = ", ebar)
#         gbar = g + zeta * U
#         Rbar = self.compute_R(gbar)
#         ebar = np.sum(np.square(Rbar))
#         zeta *= 0.7
#         if ebar < e or np.abs(ebar - e) < self.tol:
#             break
#     g = gbar
#     R = Rbar
#     e = ebar
#     k += 1
#     D = self.compute_D(g)
#     U = self.compute_U(R, D)