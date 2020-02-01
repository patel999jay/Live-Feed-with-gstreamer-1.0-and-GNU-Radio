#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Video Transceiver (GMSK)
# Author: Alexandru Csete OZ9AEC
# Generated: Sat Feb  1 01:21:53 2020
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

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx


class gmsk_trx(grc_wxgui.top_block_gui):

    def __init__(self, uri='ip:192.168.3.1'):
        grc_wxgui.top_block_gui.__init__(self, title="Video Transceiver (GMSK)")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Parameters
        ##################################################
        self.uri = uri

        ##################################################
        # Variables
        ##################################################
        self.signal = signal = 5000
        self.samp_rate = samp_rate = 2000000
        self.rfgain_tx = rfgain_tx = 0
        self.rfgain_rx = rfgain_rx = 15
        self.freq = freq = 437000000

        ##################################################
        # Blocks
        ##################################################
        _rfgain_rx_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rfgain_rx_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rfgain_rx_sizer,
        	value=self.rfgain_rx,
        	callback=self.set_rfgain_rx,
        	label='RX Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rfgain_rx_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rfgain_rx_sizer,
        	value=self.rfgain_rx,
        	callback=self.set_rfgain_rx,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_rfgain_rx_sizer)
        self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=50,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='TX FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=50,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='RX FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        _signal_sizer = wx.BoxSizer(wx.VERTICAL)
        self._signal_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_signal_sizer,
        	value=self.signal,
        	callback=self.set_signal,
        	label='Signal',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._signal_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_signal_sizer,
        	value=self.signal,
        	callback=self.set_signal,
        	minimum=0,
        	maximum=32000,
        	num_steps=320,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_signal_sizer)
        _rfgain_tx_sizer = wx.BoxSizer(wx.VERTICAL)
        self._rfgain_tx_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_rfgain_tx_sizer,
        	value=self.rfgain_tx,
        	callback=self.set_rfgain_tx,
        	label='TX Gain',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._rfgain_tx_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_rfgain_tx_sizer,
        	value=self.rfgain_tx,
        	callback=self.set_rfgain_tx,
        	minimum=0,
        	maximum=50,
        	num_steps=50,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_rfgain_tx_sizer)
        self.pluto_source_0 = iio.pluto_source(uri, freq, samp_rate, 1 - 1, 20000000, 0x8000, False, True, True, "manual", rfgain_rx, '', True)
        self.pluto_sink_0 = iio.pluto_sink(uri, freq, samp_rate, 1 - 1, 20000000, 0x8000, False, 10.0, '', True)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 350000, 50000, firdes.WIN_HAMMING, 6.76))
        self.digital_gmskmod_bc_0 = digital.gmskmod_bc(2, 4, 0.350)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
        	samples_per_symbol=2,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((30000, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/jay/txfifo.mkv', False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/jay/Desktop/pluto_sink.mkv', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=2,
        		bits_per_symbol=1,
        		preamble='',
        		access_code='',
        		pad_for_usrp=True,
        	),
        	payload_length=4000,
        )
        self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code='',
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
        	),
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_packet_decoder_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gmskmod_bc_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.pluto_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.wxgui_fftsink2_0_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
        self.connect((self.digital_gmskmod_bc_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.pluto_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.pluto_source_0, 0), (self.wxgui_fftsink2_0, 0))

    def get_uri(self):
        return self.uri

    def set_uri(self, uri):
        self.uri = uri

    def get_signal(self):
        return self.signal

    def set_signal(self, signal):
        self.signal = signal
        self._signal_slider.set_value(self.signal)
        self._signal_text_box.set_value(self.signal)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_fftsink2_0_0.set_sample_rate(self.samp_rate)
        self.wxgui_fftsink2_0.set_sample_rate(self.samp_rate)
        self.pluto_source_0.set_params(self.freq, self.samp_rate, 20000000, False, True, True, "manual", self.rfgain_rx, '', True)
        self.pluto_sink_0.set_params(self.freq, self.samp_rate, 20000000, 10.0, '', True)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 350000, 50000, firdes.WIN_HAMMING, 6.76))

    def get_rfgain_tx(self):
        return self.rfgain_tx

    def set_rfgain_tx(self, rfgain_tx):
        self.rfgain_tx = rfgain_tx
        self._rfgain_tx_slider.set_value(self.rfgain_tx)
        self._rfgain_tx_text_box.set_value(self.rfgain_tx)

    def get_rfgain_rx(self):
        return self.rfgain_rx

    def set_rfgain_rx(self, rfgain_rx):
        self.rfgain_rx = rfgain_rx
        self._rfgain_rx_slider.set_value(self.rfgain_rx)
        self._rfgain_rx_text_box.set_value(self.rfgain_rx)
        self.pluto_source_0.set_params(self.freq, self.samp_rate, 20000000, False, True, True, "manual", self.rfgain_rx, '', True)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.wxgui_fftsink2_0_0.set_baseband_freq(self.freq)
        self.wxgui_fftsink2_0.set_baseband_freq(self.freq)
        self.pluto_source_0.set_params(self.freq, self.samp_rate, 20000000, False, True, True, "manual", self.rfgain_rx, '', True)
        self.pluto_sink_0.set_params(self.freq, self.samp_rate, 20000000, 10.0, '', True)


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--uri", dest="uri", type="string", default='ip:192.168.3.1',
        help="Set URI [default=%default]")
    return parser


def main(top_block_cls=gmsk_trx, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(uri=options.uri)
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
