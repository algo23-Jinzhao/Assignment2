from template import Template
import deque
import numpy as np

class doubleMA(Template):
    def __init__(self, parameters) -> None:
        super(doubleMA, self).__init__()
        self.fast_window = parameters['fast window']
        self.slow_window = parameters['slow window']
        self._close_deque = deque(max_len=self.slow_window + 1)

    def on_bar(self, bar):
        super(doubleMA, self).on_bar(bar)

        array = self._close_deque
        array.append(bar.close)
        if len(array) != array.max_len:
            logger.debug("%s's data is not enough", self)
            return
        
        array = np.array(array)
        sma_line = talib.MA(array, self.n_sma)
        lma_line = talib.MA(array, self.l_sma)

        # up cross
        if lma_line[-1] < sma_line[-1] and lma_line[-2] >= sma_line[-2]:
            self.send_signal(self.buy())

        # down cross
        if lma_line[-1] > sma_line[-1] and lma_line[-2] <= sma_line[-2]:
            self.send_signal(self.sell())