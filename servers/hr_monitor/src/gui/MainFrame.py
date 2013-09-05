# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 on Mon Sep  2 12:11:11 2013
from __future__ import division, print_function

from time import sleep
from datetime import datetime, timedelta
from threading import current_thread
from numpy import nan, isnan

import wx
from wxmplot import PlotPanel
from PyTango import DeviceProxy

from Timer import Timer

# begin wxGlade: extracode

# end wxGlade


class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.alarm_plt = PlotPanel(self)
        self.timestamp_sld = wx.Slider(self, -1, 0, 0, 10)
        self.avg_hr_title_lbl = wx.StaticText(self, -1, "Current avg. HR:")
        self.avg_hr_lbl = wx.StaticText(self, -1, "nan")
        self.panel_1 = wx.Panel(self, -1)
        self.avg_acc_title_lbl = wx.StaticText(self, -1, "Current avg. Acceleration:")
        self.avg_acc_lbl = wx.StaticText(self, -1, "nan")
        self.panel_2 = wx.Panel(self, -1)
        self.anomaly_lvl_curr_title_lbl = wx.StaticText(self, -1, "Anomaly level: Current:")
        self.anomaly_lvl_curr_lbl = wx.StaticText(self, -1, "nan")
        self.panel_3 = wx.Panel(self, -1)
        self.anomaly_lvl_max_title_lbl = wx.StaticText(self, -1, "                                 Max:")
        self.anomaly_lvl_max_lbl = wx.StaticText(self, -1, "nan")
        self.red_alarm_lbl = wx.Panel(self, -1)
        self.anomaly_lvl_min_title_lbl = wx.StaticText(self, -1, "                                 Min:")
        self.anomaly_lvl_min_lbl = wx.StaticText(self, -1, "nan")
        self.yellow_alarm_lbl = wx.Panel(self, -1)
        self.anomaly_lvl_avg_title_lbl = wx.StaticText(self, -1, "                                 Average:")
        self.anomaly_lvl_avg_lbl = wx.StaticText(self, -1, "nan")
        self.green_alarm_lbl = wx.Panel(self, -1)
        self.collect_btn = wx.Button(self, -1, "Collect data")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_COMMAND_SCROLL, self.timestamp_sld_scroll, self.timestamp_sld)
        self.Bind(wx.EVT_BUTTON, self.collect_btn_click, self.collect_btn)
        # end wxGlade
        self.timer_thread = Timer(target=self.timer_tick)
        self.proxy = DeviceProxy('C3/hr_monitor/1')
        self.alarms = set()
        self.yellow_alrm_thrsh = 0.3
        self.red_alrm_thrsh = 0.6
        self.sleep_time = 5

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("HRMonitor GUI")
        self.red_alarm_lbl.SetBackgroundColour(wx.NullColor)
        self.yellow_alarm_lbl.SetBackgroundColour(wx.NullColor)
        self.green_alarm_lbl.SetBackgroundColour(wx.NullColor)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.GridSizer(6, 3, 0, 0)
        sizer_1.Add(self.alarm_plt, 1, wx.EXPAND, 0)
        sizer_1.Add(self.timestamp_sld, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.avg_hr_title_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.avg_hr_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.panel_1, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.avg_acc_title_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.avg_acc_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.panel_2, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.anomaly_lvl_curr_title_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.anomaly_lvl_curr_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.panel_3, 1, wx.EXPAND, 0)
        grid_sizer_2.Add(self.anomaly_lvl_max_title_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.anomaly_lvl_max_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.red_alarm_lbl, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.anomaly_lvl_min_title_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.anomaly_lvl_min_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.yellow_alarm_lbl, 0, wx.EXPAND, 0)
        grid_sizer_2.Add(self.anomaly_lvl_avg_title_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.anomaly_lvl_avg_lbl, 0, 0, 0)
        grid_sizer_2.Add(self.green_alarm_lbl, 0, wx.EXPAND, 0)
        sizer_2.Add(grid_sizer_2, 9, wx.EXPAND, 0)
        sizer_3.Add(self.collect_btn, 0, wx.ALL, 0)
        sizer_2.Add(sizer_3, 1, wx.EXPAND | wx.SHAPED, 0)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    # wxGlade: MainFrame.<event_handler>
    def timestamp_sld_scroll(self, event):
        print("Event handler `timestamp_sld_scroll' not implemented")
        event.Skip()

    # wxGlade: MainFrame.<event_handler>
    def collect_btn_click(self, event):
        if self.collect_btn.GetLabel() == "Stop collecting":
            self.collect_btn.SetLabel("Collect data")
            self.timer_thread.stop()
            del self.timer_thread
            self.timer_thread = Timer(target=self.timer_tick)
        else:
            self.collect_btn.SetLabel("Stop collecting")
            self.timer_thread.start()
        event.Skip()
# end of class MainFrame

    def timer_tick(self):
        timer = current_thread()
        proxy = self.proxy
        while not timer.stopped():
            avg_hr_idx = proxy.command_inout_asynch('get_avg_hr', 4)
            avg_acc_idx = proxy.command_inout_asynch('get_avg_acc', 4)
            alarms_idx = proxy.command_inout_asynch('get_current_alarms', 4)
            init = datetime.now()
            avg_hr = proxy.command_inout_reply(avg_hr_idx, timeout=0)
            avg_acc = proxy.command_inout_reply(avg_acc_idx, timeout=0)
            alarms = proxy.command_inout_reply(alarms_idx, timeout=0)
            sleep_time = timedelta(seconds=self.sleep_time)
            sleep_time -= (datetime.now() - init)
            sleep_time = max(sleep_time, timedelta(0)).total_seconds()
            alarms[0], alarms[1] = alarms[1], alarms[0]
            alarms[0] = [float(datetime.strptime(x, '%Y-%m-%d %H:%M:%S.%f')
                                       .strftime('%s.%f'))
                         for x in alarms[0]]
            alarms[0] = [x % 10000 for x in alarms[0]]
            if not isnan(avg_hr):
                wx.CallAfter(self.avg_hr_lbl.SetLabel, str(avg_hr))
            if not isnan(avg_acc):
                wx.CallAfter(self.avg_acc_lbl.SetLabel, str(avg_acc))
            if len(alarms[0]) > 0:
                self.alarms.update(zip(*alarms))
                wx.CallAfter(self.set_alarm_text)

            data = sorted(self.alarms)
            if len(data) > 0:
                wx.CallAfter(self.plot, zip(*data))
                wx.CallAfter(self.set_alarm_color, max(data)[1])
            sleep(sleep_time)
        del proxy

    def plot(self, data):
        x_data, y_data = data
        self.alarm_plt.plot(x_data, y_data, title="Alarm Level History")

    def set_alarm_text(self):
        alarms = sorted(self.alarms)
        if len(alarms) > 0:
            vals = [x for _, x in alarms]
        else:
            vals = [nan]
            alarms = [(nan, nan)]
        avg = sum(vals) / len(vals)
        self.anomaly_lvl_curr_lbl.SetLabel(str(alarms[-1][1]))
        self.anomaly_lvl_max_lbl.SetLabel(str(max(vals)))
        self.anomaly_lvl_min_lbl.SetLabel(str(min(vals)))
        self.anomaly_lvl_avg_lbl.SetLabel(str(avg))

    def set_alarm_color(self, alarm_lvl):
        if alarm_lvl < self.yellow_alrm_thrsh:
            self.red_alarm_lbl.SetBackgroundColour(wx.NullColor)
            self.yellow_alarm_lbl.SetBackgroundColour(wx.NullColor)
            self.green_alarm_lbl.SetBackgroundColour('Green')
        elif self.yellow_alrm_thrsh <= alarm_lvl < self.red_alrm_thrsh:
            self.red_alarm_lbl.SetBackgroundColour(wx.NullColor)
            self.yellow_alarm_lbl.SetBackgroundColour('Yellow')
            self.green_alarm_lbl.SetBackgroundColour(wx.NullColor)
        else:
            self.red_alarm_lbl.SetBackgroundColour('Red')
            self.yellow_alarm_lbl.SetBackgroundColour(wx.NullColor)
            self.green_alarm_lbl.SetBackgroundColour(wx.NullColor)
        self.red_alarm_lbl.Refresh()
        self.yellow_alarm_lbl.Refresh()
        self.green_alarm_lbl.Refresh()
        self.Refresh()
