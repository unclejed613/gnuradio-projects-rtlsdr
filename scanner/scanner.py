#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NFM SCANNER
# Author: JED MARTIN
# Description: NFM SCANNER EXPERIMENT
# Generated: Tue Jan 31 21:07:35 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from PyQt4.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import os
import osmosdr
import sip
import sys
import threading
import time


class scanner(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NFM SCANNER")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NFM SCANNER")
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "scanner")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.freqd = freqd = 0
        self.stop_scan_a = stop_scan_a = 0
        self.freq_set = freq_set = freqd
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = stop_scan_a
        self.sql = sql = -50
        self.samp_rate = samp_rate = 32000
        self.s_rate = s_rate = 2
        self.r_rate = r_rate = 240000
        self.hold_scan = hold_scan = 0
        self.gain = gain = 30
        self.frequency = frequency = freq_set/1000000

        ##################################################
        # Blocks
        ##################################################
        self.stop_scan = blocks.probe_signal_f()
        def _stop_scan_a_probe():
            while True:
                val = self.stop_scan.level()
                try:
                    self.set_stop_scan_a(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (100))
        _stop_scan_a_thread = threading.Thread(target=_stop_scan_a_probe)
        _stop_scan_a_thread.daemon = True
        _stop_scan_a_thread.start()
        self._sql_range = Range(-100, 0, 1, -50, 50)
        self._sql_win = RangeWidget(self._sql_range, self.set_sql, "squelch", "dial", float)
        self.top_layout.addWidget(self._sql_win)
        self._s_rate_options = (.5, 1, 2, 5, 10, )
        self._s_rate_labels = (".5Hz", "1Hz", "2Hz", "5Hz", "10Hz", )
        self._s_rate_tool_bar = Qt.QToolBar(self)
        self._s_rate_tool_bar.addWidget(Qt.QLabel("SCAN RATE"+": "))
        self._s_rate_combo_box = Qt.QComboBox()
        self._s_rate_tool_bar.addWidget(self._s_rate_combo_box)
        for label in self._s_rate_labels: self._s_rate_combo_box.addItem(label)
        self._s_rate_callback = lambda i: Qt.QMetaObject.invokeMethod(self._s_rate_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._s_rate_options.index(i)))
        self._s_rate_callback(self.s_rate)
        self._s_rate_combo_box.currentIndexChanged.connect(
        	lambda i: self.set_s_rate(self._s_rate_options[i]))
        self.top_layout.addWidget(self._s_rate_tool_bar)
        _hold_scan_check_box = Qt.QCheckBox("hold_scan")
        self._hold_scan_choices = {True: 1, False: 0}
        self._hold_scan_choices_inv = dict((v,k) for k,v in self._hold_scan_choices.iteritems())
        self._hold_scan_callback = lambda i: Qt.QMetaObject.invokeMethod(_hold_scan_check_box, "setChecked", Qt.Q_ARG("bool", self._hold_scan_choices_inv[i]))
        self._hold_scan_callback(self.hold_scan)
        _hold_scan_check_box.stateChanged.connect(lambda i: self.set_hold_scan(self._hold_scan_choices[bool(i)]))
        self.top_layout.addWidget(_hold_scan_check_box)
        self._gain_range = Range(0, 50, 1, 30, 25)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "GAIN", "dial", float)
        self.top_layout.addWidget(self._gain_win)
        self.freqb = blocks.probe_signal_f()
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._variable_qtgui_label_0_formatter = None
        else:
          self._variable_qtgui_label_0_formatter = lambda x: x
        
        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("scan"+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.top_layout.addWidget(self._variable_qtgui_label_0_tool_bar)
          
        self.valve = grc_blks2.valve(item_size=gr.sizeof_float*1, open=bool(stop_scan_a or hold_scan))
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "" )
        self.rtlsdr_source_0.set_sample_rate(r_rate)
        self.rtlsdr_source_0.set_center_freq(freq_set-100000, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(gain, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna("", 0)
        self.rtlsdr_source_0.set_bandwidth(r_rate, 0)
          
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq_set, #fc
        	r_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	False, #plottime
        	False, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        
        self.qtgui_sink_x_0.enable_rf_freq(True)
        
        
          
        self.low_pass_filter_0 = filter.fir_filter_ccf(5, firdes.low_pass(
        	1, r_rate, 7500, 5000, firdes.WIN_HAMMING, 6.76))
        self._frequency_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._frequency_formatter = None
        else:
          self._frequency_formatter = lambda x: x
        
        self._frequency_tool_bar.addWidget(Qt.QLabel("frequency"+": "))
        self._frequency_label = Qt.QLabel(str(self._frequency_formatter(self.frequency)))
        self._frequency_tool_bar.addWidget(self._frequency_label)
        self.top_layout.addWidget(self._frequency_tool_bar)
          
        def _freqd_probe():
            while True:
                val = self.freqb.level()
                try:
                    self.set_freqd(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (s_rate))
        _freqd_thread = threading.Thread(target=_freqd_probe)
        _freqd_thread.daemon = True
        _freqd_thread.start()
        self.freqa = blocks.file_source(gr.sizeof_float*1, "/home/jed/radio/PROJECTS/scanner/freqtest.dat", True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0.0000000001, .0001, 0)
        self.blocks_multiply_xx_2 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 10)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_sig_source_x_0 = analog.sig_source_c(r_rate, analog.GR_COS_WAVE, -100000, 1, 0)
        self.analog_pwr_squelch_xx_0 = analog.pwr_squelch_cc(sql, 1e-3, 5, False)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=r_rate / 5,
        	tau=75e-6,
        	max_dev=5.0e3,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_delay_0, 0))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_xx_1, 0))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.blocks_multiply_xx_1, 1))    
        self.connect((self.analog_pwr_squelch_xx_0, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self.audio_sink_0, 0))    
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_2, 1))    
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_2, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_sink_x_0, 0))    
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_add_xx_0, 0))    
        self.connect((self.blocks_multiply_xx_2, 0), (self.blocks_add_xx_0, 1))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.stop_scan, 0))    
        self.connect((self.freqa, 0), (self.valve, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_pwr_squelch_xx_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.blocks_multiply_xx_0, 0))    
        self.connect((self.valve, 0), (self.freqb, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "scanner")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def setStyleSheetFromFile(self, filename):
        try:
            if not os.path.exists(filename):
                filename = os.path.join(
                    gr.prefix(), "share", "gnuradio", "themes", filename)
            with open(filename) as ss:
                self.setStyleSheet(ss.read())
        except Exception as e:
            print >> sys.stderr, e

    def get_freqd(self):
        return self.freqd

    def set_freqd(self, freqd):
        self.freqd = freqd
        self.set_freq_set(self.freqd)

    def get_stop_scan_a(self):
        return self.stop_scan_a

    def set_stop_scan_a(self, stop_scan_a):
        self.stop_scan_a = stop_scan_a
        self.set_variable_qtgui_label_0(self._variable_qtgui_label_0_formatter(self.stop_scan_a))
        self.valve.set_open(bool(self.stop_scan_a or self.hold_scan))

    def get_freq_set(self):
        return self.freq_set

    def set_freq_set(self, freq_set):
        self.freq_set = freq_set
        self.set_frequency(self._frequency_formatter(self.freq_set/1000000))
        self.qtgui_sink_x_0.set_frequency_range(self.freq_set, self.r_rate)
        self.rtlsdr_source_0.set_center_freq(self.freq_set-100000, 0)

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", str(self.variable_qtgui_label_0)))

    def get_sql(self):
        return self.sql

    def set_sql(self, sql):
        self.sql = sql
        self.analog_pwr_squelch_xx_0.set_threshold(self.sql)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_s_rate(self):
        return self.s_rate

    def set_s_rate(self, s_rate):
        self.s_rate = s_rate
        self._s_rate_callback(self.s_rate)

    def get_r_rate(self):
        return self.r_rate

    def set_r_rate(self, r_rate):
        self.r_rate = r_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.r_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.r_rate, 7500, 5000, firdes.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0.set_frequency_range(self.freq_set, self.r_rate)
        self.rtlsdr_source_0.set_sample_rate(self.r_rate)
        self.rtlsdr_source_0.set_bandwidth(self.r_rate, 0)

    def get_hold_scan(self):
        return self.hold_scan

    def set_hold_scan(self, hold_scan):
        self.hold_scan = hold_scan
        self._hold_scan_callback(self.hold_scan)
        self.valve.set_open(bool(self.stop_scan_a or self.hold_scan))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.rtlsdr_source_0.set_gain(self.gain, 0)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        Qt.QMetaObject.invokeMethod(self._frequency_label, "setText", Qt.Q_ARG("QString", str(self.frequency)))


def main(top_block_cls=scanner, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.setStyleSheetFromFile('/home/jed/radio/dark.qss')
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
