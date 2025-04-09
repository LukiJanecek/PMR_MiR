# PMR_MiR
PMR project 

pip install requests

pip install requests matplotlib

Traceback (most recent call last):
  File "c:\Python311\Lib\tkinter\__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 188, in startMission
    self.process_data_ui()
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 217, in process_data_ui
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 231, in update_plot
    for val in values:
TypeError: 'bool' object is not iterable
Exception in Tkinter callback
Traceback (most recent call last):
  File "c:\Python311\Lib\tkinter\__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 188, in startMission
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 217, in process_data_ui
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 231, in update_plot
    for val in values:
TypeError: 'bool' object is not iterable

Measured values: (True, [], [])
Measured values: (True, [], [])
Measured values: (True, [], [])
Exception in Tkinter callback
Traceback (most recent call last):
  File "c:\Python311\Lib\tkinter\__init__.py", line 1948, in __call__
    return self.func(*args)
           ^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 188, in startMission
    self.process_data_ui()
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 217, in process_data_ui
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_axes.py", line 1777, in plot
    lines = [*self._get_lines(self, *args, data=data, **kwargs)]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 297, in __call__
    yield from self._plot_args(
               ^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 486, in _plot_args
    x, y = index_of(xy[-1])
           ^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\cbook.py", line 1672, in index_of
    raise ValueError('Input could not be cast to an at-least-1D NumPy array')
ValueError: Input could not be cast to an at-least-1D NumPy array




    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_axes.py", line 1777, in plot
    lines = [*self._get_lines(self, *args, data=data, **kwargs)]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 297, in __call__
    yield from self._plot_args(
               ^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 486, in _plot_args
    x, y = index_of(xy[-1])
           ^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\cbook.py", line 1672, in index_of
    raise ValueError('Input could not be cast to an at-least-1D NumPy array')
ValueError: Input could not be cast to an at-least-1D NumPy array

    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_axes.py", line 1777, in plot
    lines = [*self._get_lines(self, *args, data=data, **kwargs)]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 297, in __call__
    yield from self._plot_args(
               ^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 486, in _plot_args
    x, y = index_of(xy[-1])
           ^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\cbook.py", line 1672, in index_of
    raise ValueError('Input could not be cast to an at-least-1D NumPy array')
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_axes.py", line 1777, in plot
    lines = [*self._get_lines(self, *args, data=data, **kwargs)]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 297, in __call__
    yield from self._plot_args(
               ^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 486, in _plot_args
    x, y = index_of(xy[-1])
           ^^^^^^^^^^^^^^^^
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_axes.py", line 1777, in plot
    lines = [*self._get_lines(self, *args, data=data, **kwargs)]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 297, in __call__
    yield from self._plot_args(
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.update_plot()  # Spuštění automatického refreshu
    ^^^^^^^^^^^^^^^^^^
    ^^^^^^^^^^^^^^^^^^
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
  File "d:\VS\Projekty\TACR_SIGMA_DC2\PMR_MiR\MiR_DataCollection\MiR_GUI.py", line 237, in update_plot
    self.ax.plot(values, marker='o', linestyle='-')
    self.ax.plot(values, marker='o', linestyle='-')
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_axes.py", line 1777, in plot
    lines = [*self._get_lines(self, *args, data=data, **kwargs)]
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 297, in __call__
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 297, in __call__
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 297, in __call__
    yield from self._plot_args(
  File "c:\Python311\Lib\site-packages\matplotlib\axes\_base.py", line 486, in _plot_args
           ^^^^^^^^^^^^^^^^
  File "c:\Python311\Lib\site-packages\matplotlib\cbook.py", line 1672, in index_of
    raise ValueError('Input could not be cast to an at-least-1D NumPy array')
ValueError: Input could not be cast to an at-least-1D NumPy array