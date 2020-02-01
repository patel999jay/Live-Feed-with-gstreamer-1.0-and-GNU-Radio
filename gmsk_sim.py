#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: DVB Simulator (GMSK)
# Author: JAY PATEL
# Description: Live Webcam Feed
# Generated: Sat Feb  1 19:17:49 2020
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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
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


class gmsk_sim(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="DVB Simulator (GMSK)")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.signal = signal = 500
        self.samp_rate = samp_rate = 1024
        self.noise = noise = 10

        ##################################################
        # Blocks
        ##################################################
        _noise_sizer = wx.BoxSizer(wx.VERTICAL)
        self._noise_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_noise_sizer,
        	value=self.noise,
        	callback=self.set_noise,
        	label='Noise',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._noise_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_noise_sizer,
        	value=self.noise,
        	callback=self.set_noise,
        	minimum=0,
        	maximum=1000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_noise_sizer)
        self.wxgui_fftsink2_0_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=0,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='RX FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0_0.win)
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
        	maximum=1000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_signal_sizer)
        self.digital_gmskmod_bc_0 = digital.gmskmod_bc(2, 4, 0.3)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
        	samples_per_symbol=2,
        	gain_mu=0.175,
        	mu=0.5,
        	omega_relative_limit=0.005,
        	freq_error=0.0,
        	verbose=False,
        	log=False,
        )
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((500, ))
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/jay/txfifo.mkv', False)
        self.blocks_file_sink_0_0 = blocks.file_sink(gr.sizeof_char*1, '/home/jay/Desktop/sink.mkv', False)
        self.blocks_file_sink_0_0.set_unbuffered(False)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, '/home/jay/Desktop/sink.mkv', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(grc_blks2.packet_encoder(
        		samples_per_symbol=2,
        		bits_per_symbol=1,
        		preamble='',
        		access_code='',
        		pad_for_usrp=True,
        	),
        	payload_length=0,
        )
        self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
        		access_code='',
        		threshold=-1,
        		callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
        	),
        )
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise, 42)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blks2_packet_decoder_0, 0), (self.blocks_file_sink_0_0, 0))
        self.connect((self.blks2_packet_encoder_0, 0), (self.digital_gmskmod_bc_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.wxgui_fftsink2_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blks2_packet_encoder_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
        self.connect((self.digital_gmskmod_bc_0, 0), (self.blocks_multiply_const_vxx_0, 0))

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

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self._noise_slider.set_value(self.noise)
        self._noise_text_box.set_value(self.noise)
        self.analog_noise_source_x_0.set_amplitude(self.noise)


def main(top_block_cls=gmsk_sim, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
