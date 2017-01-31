#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: COMMUNICATIONS-RECEIVER
# Author: JED MARTIN
# Description: AM-FM-SSB RECEIVER FOR RTL-SDR
# Generated: Sat Jan 21 23:41:39 2017
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
import time


class commrx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "COMMUNICATIONS-RECEIVER")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("COMMUNICATIONS-RECEIVER")
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

        self.settings = Qt.QSettings("GNU Radio", "commrx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.upconv = upconv = 0
        self.rit = rit = 0
        self.ften = ften = 50000000
        self.fsel = fsel = 0
        self.fone = fone = 5000000
        self.fhun = fhun = 100000000
        self.squelch = squelch = -70
        self.scanw = scanw = 1000000
        self.samp_rate = samp_rate = 1200000
        self.msel = msel = 1
        self.gain = gain = 35
        self.freq = freq = fhun+ften+fone+fsel+rit-100000
        self.corr = corr = 3
        self.FREQUENCY = FREQUENCY = ((upconv+fhun+ften+fone+fsel+rit)/1000000)

        ##################################################
        # Blocks
        ##################################################
        self._squelch_range = Range(-80, -20, 1, -70, 50)
        self._squelch_win = RangeWidget(self._squelch_range, self.set_squelch, "squelch", "dial", float)
        self.top_grid_layout.addWidget(self._squelch_win, 5,3,1,1)
        self._scanw_range = Range(10000, 1000000, 10000, 1000000, 50)
        self._scanw_win = RangeWidget(self._scanw_range, self.set_scanw, "scanw", "counter", float)
        self.top_grid_layout.addWidget(self._scanw_win, 6,0,1,2)
        self._msel_options = (0, 1, 2, 3, 4, )
        self._msel_labels = ("AM", "NFM", "WFM", "USB", "LSB", )
        self._msel_group_box = Qt.QGroupBox("MODE")
        self._msel_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._msel_button_group = variable_chooser_button_group()
        self._msel_group_box.setLayout(self._msel_box)
        for i, label in enumerate(self._msel_labels):
        	radio_button = Qt.QRadioButton(label)
        	self._msel_box.addWidget(radio_button)
        	self._msel_button_group.addButton(radio_button, i)
        self._msel_callback = lambda i: Qt.QMetaObject.invokeMethod(self._msel_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._msel_options.index(i)))
        self._msel_callback(self.msel)
        self._msel_button_group.buttonClicked[int].connect(
        	lambda i: self.set_msel(self._msel_options[i]))
        self.top_grid_layout.addWidget(self._msel_group_box, 1,3,1,1)
        self._gain_range = Range(0, 50, 1, 35, 50)
        self._gain_win = RangeWidget(self._gain_range, self.set_gain, "gain", "dial", float)
        self.top_grid_layout.addWidget(self._gain_win, 4,3,1,1)
        _upconv_check_box = Qt.QCheckBox("UPCONVERTER")
        self._upconv_choices = {True: -125000000, False: 0}
        self._upconv_choices_inv = dict((v,k) for k,v in self._upconv_choices.iteritems())
        self._upconv_callback = lambda i: Qt.QMetaObject.invokeMethod(_upconv_check_box, "setChecked", Qt.Q_ARG("bool", self._upconv_choices_inv[i]))
        self._upconv_callback(self.upconv)
        _upconv_check_box.stateChanged.connect(lambda i: self.set_upconv(self._upconv_choices[bool(i)]))
        self.top_grid_layout.addWidget(_upconv_check_box, 1,4,1,1)
        self._rit_range = Range(-500, 500, 10, 0, 50)
        self._rit_win = RangeWidget(self._rit_range, self.set_rit, "RIT", "dial", float)
        self.top_grid_layout.addWidget(self._rit_win, 2,1,1,1)
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	512, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	(freq+100000), #fc
        	scanw, #bw
        	"", #name
        	False, #plotfreq
        	True, #plotwaterfall
        	False, #plottime
        	False, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 5,0,1,2)
        
        self.qtgui_sink_x_0.enable_rf_freq(True)
        
        
          
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	freq+100000, #fc
        	scanw, #bw
        	"RF", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.2)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        
        if not True:
          self.qtgui_freq_sink_x_0.disable_legend()
        
        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["green", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 4,0,1,2)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "RTL2838UHIDIR" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(freq, 0)
        self.osmosdr_source_0.set_freq_corr(corr, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(samp_rate, 0)
          
        (self.osmosdr_source_0).set_min_output_buffer(8)
        (self.osmosdr_source_0).set_max_output_buffer(32)
        self.msel1 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=1,
        	num_outputs=5,
        	input_index=0,
        	output_index=msel,
        )
        self.low_pass_filter_0_1 = filter.fir_filter_ccf(5, firdes.low_pass(
        	1, samp_rate, 75000, 25000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(25, firdes.low_pass(
        	1, samp_rate, 5000, 5000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(25, firdes.low_pass(
        	1, samp_rate, 7500, 5000, firdes.WIN_HAMMING, 6.76))
        self._ften_range = Range(0, 90000000, 10000000, 50000000, 50)
        self._ften_win = RangeWidget(self._ften_range, self.set_ften, "10s", "dial", float)
        self.top_grid_layout.addWidget(self._ften_win, 1,0,1,1)
        self._fsel_range = Range(0, 999000, 1000, 0, 1000)
        self._fsel_win = RangeWidget(self._fsel_range, self.set_fsel, "fsel", "counter_slider", float)
        self.top_grid_layout.addWidget(self._fsel_win, 0,0,1,2)
        self._fone_range = Range(0, 9000000, 1000000, 5000000, 50)
        self._fone_win = RangeWidget(self._fone_range, self.set_fone, "1s", "dial", float)
        self.top_grid_layout.addWidget(self._fone_win, 1,1,1,1)
        self._fhun_range = Range(0, 2000000000, 100000000, 100000000, 50)
        self._fhun_win = RangeWidget(self._fhun_range, self.set_fhun, "100s", "counter", float)
        self.top_grid_layout.addWidget(self._fhun_win, 2,0,1,1)
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(32, True)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_complex_to_real_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.band_pass_filter_0_0 = filter.fir_filter_ccc(25, firdes.complex_band_pass(
        	1, samp_rate, -2800, 200, 1000, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0 = filter.fir_filter_ccc(25, firdes.complex_band_pass(
        	1, samp_rate, 200, 2800, 1000, firdes.WIN_HAMMING, 6.76))
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.asel = grc_blks2.selector(
        	item_size=gr.sizeof_float*1,
        	num_inputs=5,
        	num_outputs=1,
        	input_index=msel,
        	output_index=0,
        )
        self.analog_wfm_rcv_0 = analog.wfm_rcv(
        	quad_rate=samp_rate / 5,
        	audio_decimation=5,
        )
        self.analog_simple_squelch_cc_4 = analog.simple_squelch_cc(squelch, 1)
        self.analog_simple_squelch_cc_3 = analog.simple_squelch_cc(squelch, 1)
        self.analog_simple_squelch_cc_2 = analog.simple_squelch_cc(squelch, 1)
        self.analog_simple_squelch_cc_1 = analog.simple_squelch_cc(squelch, 1)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(squelch, 1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -100000, 1, 0)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=48000,
        	quad_rate=samp_rate/25,
        	tau=75e-6,
        	max_dev=5.0e3,
        )
        self.analog_agc_xx_0_1 = analog.agc_ff(1e-1, 0.02, 1.0)
        self.analog_agc_xx_0_1.set_max_gain(65536)
        self.analog_agc_xx_0_0 = analog.agc_ff(1e-1, 0.02, 1.0)
        self.analog_agc_xx_0_0.set_max_gain(65536)
        self.analog_agc_xx_0 = analog.agc_ff(1e-1, 0.02, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)
        self._FREQUENCY_tool_bar = Qt.QToolBar(self)
        
        if None:
          self._FREQUENCY_formatter = None
        else:
          self._FREQUENCY_formatter = lambda x: x
        
        self._FREQUENCY_tool_bar.addWidget(Qt.QLabel("FREQUENCY"+": "))
        self._FREQUENCY_label = Qt.QLabel(str(self._FREQUENCY_formatter(self.FREQUENCY)))
        self._FREQUENCY_tool_bar.addWidget(self._FREQUENCY_label)
        self.top_grid_layout.addWidget(self._FREQUENCY_tool_bar, 3,0,1,1)
          

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc_xx_0, 0), (self.asel, 0))    
        self.connect((self.analog_agc_xx_0_0, 0), (self.asel, 3))    
        self.connect((self.analog_agc_xx_0_1, 0), (self.asel, 4))    
        self.connect((self.analog_nbfm_rx_0, 0), (self.asel, 1))    
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))    
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.analog_simple_squelch_cc_1, 0), (self.analog_nbfm_rx_0, 0))    
        self.connect((self.analog_simple_squelch_cc_2, 0), (self.analog_wfm_rcv_0, 0))    
        self.connect((self.analog_simple_squelch_cc_3, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.analog_simple_squelch_cc_4, 0), (self.blocks_complex_to_real_0_0, 0))    
        self.connect((self.analog_wfm_rcv_0, 0), (self.asel, 2))    
        self.connect((self.asel, 0), (self.audio_sink_0, 0))    
        self.connect((self.band_pass_filter_0, 0), (self.analog_simple_squelch_cc_3, 0))    
        self.connect((self.band_pass_filter_0_0, 0), (self.analog_simple_squelch_cc_4, 0))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.dc_blocker_xx_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.analog_agc_xx_0_0, 0))    
        self.connect((self.blocks_complex_to_real_0_0, 0), (self.analog_agc_xx_0_1, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.msel1, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_freq_sink_x_0, 0))    
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_sink_x_0, 0))    
        self.connect((self.dc_blocker_xx_0, 0), (self.analog_agc_xx_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.analog_simple_squelch_cc_1, 0))    
        self.connect((self.low_pass_filter_0_0, 0), (self.analog_simple_squelch_cc_0, 0))    
        self.connect((self.low_pass_filter_0_1, 0), (self.analog_simple_squelch_cc_2, 0))    
        self.connect((self.msel1, 3), (self.band_pass_filter_0, 0))    
        self.connect((self.msel1, 4), (self.band_pass_filter_0_0, 0))    
        self.connect((self.msel1, 1), (self.low_pass_filter_0, 0))    
        self.connect((self.msel1, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.msel1, 2), (self.low_pass_filter_0_1, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "commrx")
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

    def get_upconv(self):
        return self.upconv

    def set_upconv(self, upconv):
        self.upconv = upconv
        self.set_FREQUENCY(self._FREQUENCY_formatter(((self.upconv+self.fhun+self.ften+self.fone+self.fsel+self.rit)/1000000)))
        self._upconv_callback(self.upconv)

    def get_rit(self):
        return self.rit

    def set_rit(self, rit):
        self.rit = rit
        self.set_FREQUENCY(self._FREQUENCY_formatter(((self.upconv+self.fhun+self.ften+self.fone+self.fsel+self.rit)/1000000)))
        self.set_freq(self.fhun+self.ften+self.fone+self.fsel+self.rit-100000)

    def get_ften(self):
        return self.ften

    def set_ften(self, ften):
        self.ften = ften
        self.set_FREQUENCY(self._FREQUENCY_formatter(((self.upconv+self.fhun+self.ften+self.fone+self.fsel+self.rit)/1000000)))
        self.set_freq(self.fhun+self.ften+self.fone+self.fsel+self.rit-100000)

    def get_fsel(self):
        return self.fsel

    def set_fsel(self, fsel):
        self.fsel = fsel
        self.set_FREQUENCY(self._FREQUENCY_formatter(((self.upconv+self.fhun+self.ften+self.fone+self.fsel+self.rit)/1000000)))
        self.set_freq(self.fhun+self.ften+self.fone+self.fsel+self.rit-100000)

    def get_fone(self):
        return self.fone

    def set_fone(self, fone):
        self.fone = fone
        self.set_FREQUENCY(self._FREQUENCY_formatter(((self.upconv+self.fhun+self.ften+self.fone+self.fsel+self.rit)/1000000)))
        self.set_freq(self.fhun+self.ften+self.fone+self.fsel+self.rit-100000)

    def get_fhun(self):
        return self.fhun

    def set_fhun(self, fhun):
        self.fhun = fhun
        self.set_FREQUENCY(self._FREQUENCY_formatter(((self.upconv+self.fhun+self.ften+self.fone+self.fsel+self.rit)/1000000)))
        self.set_freq(self.fhun+self.ften+self.fone+self.fsel+self.rit-100000)

    def get_squelch(self):
        return self.squelch

    def set_squelch(self, squelch):
        self.squelch = squelch
        self.analog_simple_squelch_cc_0.set_threshold(self.squelch)
        self.analog_simple_squelch_cc_1.set_threshold(self.squelch)
        self.analog_simple_squelch_cc_2.set_threshold(self.squelch)
        self.analog_simple_squelch_cc_3.set_threshold(self.squelch)
        self.analog_simple_squelch_cc_4.set_threshold(self.squelch)

    def get_scanw(self):
        return self.scanw

    def set_scanw(self, scanw):
        self.scanw = scanw
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq+100000, self.scanw)
        self.qtgui_sink_x_0.set_frequency_range((self.freq+100000), self.scanw)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.band_pass_filter_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, 200, 2800, 1000, firdes.WIN_HAMMING, 6.76))
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.samp_rate, -2800, 200, 1000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 7500, 5000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 5000, 5000, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.samp_rate, 75000, 25000, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_bandwidth(self.samp_rate, 0)

    def get_msel(self):
        return self.msel

    def set_msel(self, msel):
        self.msel = msel
        self._msel_callback(self.msel)
        self.asel.set_input_index(int(self.msel))
        self.msel1.set_output_index(int(self.msel))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.osmosdr_source_0.set_gain(self.gain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.freq+100000, self.scanw)
        self.qtgui_sink_x_0.set_frequency_range((self.freq+100000), self.scanw)
        self.osmosdr_source_0.set_center_freq(self.freq, 0)

    def get_corr(self):
        return self.corr

    def set_corr(self, corr):
        self.corr = corr
        self.osmosdr_source_0.set_freq_corr(self.corr, 0)

    def get_FREQUENCY(self):
        return self.FREQUENCY

    def set_FREQUENCY(self, FREQUENCY):
        self.FREQUENCY = FREQUENCY
        Qt.QMetaObject.invokeMethod(self._FREQUENCY_label, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.FREQUENCY)))


def main(top_block_cls=commrx, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.setStyleSheetFromFile('dark.qss')
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
