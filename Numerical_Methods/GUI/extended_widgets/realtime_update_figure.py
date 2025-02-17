import matplotlib.backend_tools as mb_tools, matplotlib.backend_managers as mb_managers, matplotlib.backends.backend_tkagg as mb_tkagg
import matplotlib.figure
import tkinter as tk
import numpy as np
import threading, time, sched, signal

class RealTimeFigure(tk.Frame):
    
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.figure = matplotlib.figure.Figure()
        self.canvas = mb_tkagg.FigureCanvasTkAgg(self.figure,master=self)
        self.frame = np.zeros((200,200))
        self.swapchain = [self.frame] + [ self.frame.copy() for i in range(max(1,int(kwargs.get('buff_size',1)-1)))]
        self.swpachain_size =kwargs.get('buff_size',0)
        self.framebuffer = None
        if len(self.swapchain)<2:
            self._framebuffer = 0
        else:
            self._framebuffer = 1
            
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        # self.toolbar = mb_tkagg.NavigationToolbar2Tk(self.canvas,self)
        # self.toolbar.update()
        self.pack()
        self.figure.clear(False)
        self.figure
        self.update_thread = None
        self._should_run_thread = False
    
    def get_tk_widget(self):
        return self.canvas.get_tk_widget()
    
    def draw(self):
       self.frame=self.swapchain[self.framebuffer]
       self.framebuffer = (self.framebuffer+1)%self.swpachain_size
       [[ax,*_],*_] = self.figure.axes
       ax.imshow(self.frame)
       self.canvas.draw()
       
    def _loop(self):
        self.draw()
    def _start(self):
        pass
    def _stop(self):
        pass
    
    def _realtime_loop(self):
        self._start()
        try:
            while self._should_run_thread:
                self._loop()
                self.update()
        except Exception as e:
            self._stop()
            raise e
        finally:
            self._stop()
            self.update_thread=None
    
    def start_async_update_thread(self):
        if self.update_thread is None:
            self.update_thread = threading.Timer(0.1,self._realtime_loop)
        else:
            raise threading.ThreadError('The realtime thread is already running you must stop it before you can a new one!')
    
    def update(self):
        super().update()


def timerFactory():
    clock = 0
    def timer():
        print('Clock polled at', time.perf_counter(),f"tick={timer.__dict__.get('t')}")
        nonlocal clock
        retval = clock
        clock+=1
        timer.__dict__.update(t=retval)
        return retval
    timer.__dict__.update(t=0)
    def delayer(DEL):
        return 
    
    return timer,delayer
    
if __name__ == '__main__':
    # counter,delayC = timerFactory()
    # rlayer = sched.scheduler(timefunc=counter,delayfunc=delayC)
    # print('inited tiner')
    
    # rlayer.enter(22,0,lambda:print('elem',22,counter.__dict__.get('t')))
    # print('Added Wait time',22)
    
    # rlayer.enter(8,0,lambda:print('elem',8,counter.__dict__.get('t')))
    # print('Added Wait time',8) 
    
    # rlayer.enter(16,0,lambda:print("Hello\nWorld!"))
    # print('Added Wait time',16)
    
    # rlayer.enter(12,99,lambda:print('elem',12,counter.__dict__.get('t')))
    # print('Added Wait time',12)
    
    # rlayer.enter(5.6,0,lambda:print('elem',5.6,counter.__dict__.get('t')))
    # print('Added Wait time',5.6)
    
    # rlayer.enter(4,0,lambda:print('elem',4,counter.__dict__.get('t')))
    # print('Added Wait time',4)
    
    # rlayer.run(True)
    root= tk.Tk()
    figureFrame = RealTimeFigure(root)
    figureFrame.pack()
    ax=figureFrame.figure.add_subplot(111)
    ax.plot(xs:=[i for i in range(200)],np.sin(xs))
    figureFrame.canvas.draw()
    root.mainloop()