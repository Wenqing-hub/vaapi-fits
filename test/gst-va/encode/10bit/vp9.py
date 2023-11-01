###
### Copyright (C) 2023 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from .....lib import *
from .....lib.gstreamer.va.util import *
from .....lib.gstreamer.va.encoder import VP9_10EncoderTest, VP9_10EncoderLPTest

spec = load_test_spec("vp9", "encode", "10bit")

class cqp(VP9_10EncoderTest):
  def init(self, tspec, case, ipmode, qp, quality, looplvl, loopshp):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      case      = case,
      gop       = 30 if ipmode != 0 else 1,
      looplvl   = looplvl,
      loopshp   = loopshp,
      qp        = qp,
      quality   = quality,
      rcmode    = "cqp",
    )

  @parametrize_with_unused(*gen_vp9_cqp_parameters(spec), ['slices','refmode'])
  def test(self, case, ipmode, qp, quality, slices, refmode, looplvl, loopshp):
    self.init(spec, case, ipmode, qp, quality, looplvl, loopshp)
    self.encode()

class cbr(VP9_10EncoderTest):
  def init(self, tspec, case, gop, bitrate, fps, looplvl, loopshp):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      frames    = vars(self).get("brframes", self.frames),
      gop       = gop,
      looplvl   = looplvl,
      loopshp   = loopshp,
      maxrate   = bitrate,
      minrate   = bitrate,
      rcmode    = "cbr",
    )

  @parametrize_with_unused(*gen_vp9_cbr_parameters(spec), ['slices','refmode'])
  def test(self, case, gop, bitrate, fps, slices, refmode, looplvl, loopshp):
    self.init(spec, case, gop, bitrate, fps, looplvl, loopshp)
    self.encode()

class vbr(VP9_10EncoderTest):
  def init(self, tspec, case, gop, bitrate, fps, quality, looplvl, loopshp):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      frames    = vars(self).get("brframes", self.frames),
      gop       = gop,
      looplvl   = looplvl,
      loopshp   = loopshp,
      # target percentage 50%
      maxrate   = bitrate * 2,
      minrate   = bitrate,
      quality   = quality,
      rcmode    = "vbr",
    )

  @parametrize_with_unused(*gen_vp9_vbr_parameters(spec), ['slices','refmode'])
  def test(self, case, gop, bitrate, fps, quality, slices, refmode, looplvl, loopshp):
    self.init(spec, case, gop, bitrate, fps, quality, looplvl, loopshp)
    self.encode()

class cqp_lp(VP9_10EncoderLPTest):
  def init(self, tspec, case, ipmode, qp, quality, looplvl, loopshp):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      case      = case,
      gop       = 30 if ipmode != 0 else 1,
      looplvl   = looplvl,
      loopshp   = loopshp,
      qp        = qp,
      quality   = quality,
      rcmode    = "cqp",
    )

  @parametrize_with_unused(*gen_vp9_cqp_lp_parameters(spec), ['slices','refmode'])
  def test(self, case, ipmode, qp, quality, slices, refmode, looplvl, loopshp):
    self.init(spec, case, ipmode, qp, quality, looplvl, loopshp)
    self.encode()

class cbr_lp(VP9_10EncoderLPTest):
  def init(self, tspec, case, gop, bitrate, fps, looplvl, loopshp):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      frames    = vars(self).get("brframes", self.frames),
      gop       = gop,
      looplvl   = looplvl,
      loopshp   = loopshp,
      maxrate   = bitrate,
      minrate   = bitrate,
      rcmode    = "cbr",
    )

  @parametrize_with_unused(*gen_vp9_cbr_lp_parameters(spec), ['slices','refmode'])
  def test(self, case, gop, bitrate, fps, slices, refmode, looplvl, loopshp):
    self.init(spec, case, gop, bitrate, fps, looplvl, loopshp)
    self.encode()

class vbr_lp(VP9_10EncoderLPTest):
  def init(self, tspec, case, gop, bitrate, fps, quality, looplvl, loopshp):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      frames    = vars(self).get("brframes", self.frames),
      gop       = gop,
      looplvl   = looplvl,
      loopshp   = loopshp,
      # target percentage 50%
      maxrate   = bitrate * 2,
      minrate   = bitrate,
      quality   = quality,
      rcmode    = "vbr",
    )

  @parametrize_with_unused(*gen_vp9_vbr_lp_parameters(spec), ['slices','refmode'])
  def test(self, case, gop, bitrate, fps, quality, slices, refmode, looplvl, loopshp):
    self.init(spec, case, gop, bitrate, fps, quality, looplvl, loopshp)
    self.encode()
