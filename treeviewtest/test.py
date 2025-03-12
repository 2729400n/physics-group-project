def func(self):
    if self.current_task is None:
        return
    backup_old_store = {i:self.stores[i].get() for i in self.stores}
    _to_clear = {i:(self._to_clear.get(i,0)+1) for i in self.stores}
    for i in _to_clear :
        if _to_clear.get(i,0)>=2:
            self.stores.pop(i,None)
            self._to_clear.pop(i,None)
            
    if self.Iframe is not None:
        self.Iframe.destroy()
        
    Iframe=self.Iframe = ttk.Frame(self.inner_frame)
    self.Iframe.pack(expand=True,fill=tk.BOTH,anchor=tk.NW,padx=5,pady=5)
    self.Iframe.propagate(True)
    if len(self.current_task.exposed_methods) == 0:
        self.stores.update(**py_iface.makeFunctionCallable(
            self.current_task.setup, self.Iframe, classType=True,
            instance=self.current_task))
        self.stores.update(**py_iface.makeFunctionCallable(
            self.current_task.run, self.Iframe, classType=True,
            instance=self.current_task))
        self.stores.update(**py_iface.makeFunctionCallable(
            self.current_task._show_Efield, self.Iframe, classType=True, instance=self.current_task))
    else:
        for i in self.current_task.exposed_methods:
            self.stores.update(**py_iface.makeFunctionCallable(
                i, self.Iframe, classType=True, instance=self.current_task))
    for i in self.stores:
        old_value=backup_old_store.get(i)
        if old_value is None:
            continue
        try:
            self.stores[i].set(old_value)
        except:
            pass
    if self.current_task.figure is None:
        self.current_task.figure = matplotlib.figure.Figure(figsize=(8, 8), dpi=64, tight_layout=True)
    self._display.figure = self.current_task.figure
    self.ctask_str.set(f"Task: {self.current_task.name}")