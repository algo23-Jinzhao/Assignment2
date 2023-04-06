# module 1: engine->成交 to position->计算盈亏
DataEngine->行情读取bar数据，发送到event
OrderEngine->接收order->发送成交价格与数量到event

# module 2: 事件处理器->event
DataEvent: get_data & set_data->传递行情数据到signal
SignalEvent: get_signal & send_signal->接收signal并传递到order
OrderEvent: get_order & send_order->接收engine的order成交信息返回给pms

# module 3: strategy->signal
template: get_market & send_signal

# module 4: order manager->order to engine
OrderManager: get_signal & send_signal->止盈止损

# module 5: position manager->position(更新仓位)
PositionManager: 
get_signal& send_order->检查资金，有资金则冻结，发出订单到engine
get_order & get_pnl->计算盈亏

# module 6: performance
PerformanceAttribution