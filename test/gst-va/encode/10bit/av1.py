###
### Copyright (C) 2023 Intel Corporation
###
### SPDX-License-Identifier: BSD-3-Clause
###

from .....lib import *
from .....lib.gstreamer.va.util import *
from .....lib.gstreamer.va.encoder import EncoderTest

spec = load_test_spec("av1", "encode", "10bit")
spec_r2r  = load_test_spec("av1", "encode", "10bit", "r2r")

@slash.requires(*have_gst_element("vaav1dec"))
class AV1EncoderBaseTest(EncoderTest):
  def before(self):
    super().before()
    vars(self).update(
      codec         = "av1-10",
      gstdecoder    = "vaav1dec",
      gstmediatype  = "video/x-av1",
      gstmuxer      = "matroskamux",
      gstdemuxer    = "matroskademux",
      gstparser     = "av1parse",
    )

  def get_file_ext(self):
    return "webm"

@slash.requires(*have_gst_element("vaav1enc"))
@slash.requires(*platform.have_caps("encode", "av1_10"))
class AV1EncoderTest(AV1EncoderBaseTest):
  def before(self):
    super().before()
    vars(self).update(
      caps        = platform.get_caps("encode", "av1_10"),
      gstencoder  = "vaav1enc",
      lowpower    = False,
    )

@slash.requires(*have_gst_element("vaav1lpenc"))
@slash.requires(*platform.have_caps("vdenc", "av1_10"))
class AV1EncoderLPTest(AV1EncoderBaseTest):
  def before(self):
    super().before()
    vars(self).update(
      caps        = platform.get_caps("vdenc", "av1_10"),
      gstencoder  = "vaav1lpenc",
      lowpower    = True,
    )

class cqp(AV1EncoderTest):
  def init(self, tspec, case, gop, bframes, tilecols, tilerows,qp, quality, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      case      = case,
      gop       = gop,
      bframes   = bframes,
      qp        = qp,
      rcmode    = "cqp",
      quality   = quality,
      profile   = profile,
      tilerows  = tilerows,
      tilecols  = tilecols,
    )

  @slash.parametrize(*gen_av1_cqp_parameters(spec))
  def test(self, case, gop, bframes, tilecols, tilerows, qp, quality, profile):
    self.init(spec, case, gop, bframes, tilecols, tilerows, qp, quality, profile)
    self.encode()

  @slash.parametrize(*gen_av1_cqp_parameters(spec_r2r))
  def test_r2r(self, case, gop, bframes, tilecols, tilerows, qp, quality, profile):
    self.init(spec_r2r, case, gop, bframes, tilecols, tilerows, qp, quality, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()


class cbr(AV1EncoderTest):
  def init(self, tspec, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      gop       = gop,
      maxrate   = bitrate,
      minrate   = bitrate,
      profile   = profile,
      rcmode    = "cbr",
      tilerows  = tilerows,
      tilecols  = tilecols,
      quality   = quality,
      bframes   = bframes,
    )

  @slash.parametrize(*gen_av1_cbr_parameters(spec))
  def test(self, case, gop, bframes, tilecols, tilerows, bitrate, quality, fps, profile):
    self.init(spec, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile)
    self.encode()

  @slash.parametrize(*gen_av1_cbr_parameters(spec_r2r))
  def test_r2r(self, case, gop, bframes, tilecols, tilerows, bitrate, quality, fps, profile):
    self.init(spec_r2r, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

class vbr(AV1EncoderTest):
  def init(self, tspec, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      gop       = gop,
      maxrate   = bitrate * 2, # target percentage 50%
      minrate   = bitrate,
      profile   = profile,
      rcmode    = "vbr",
      tilerows  = tilerows,
      tilecols  = tilecols,
      quality   = quality,
      bframes   = bframes,
    )

  @slash.parametrize(*gen_av1_vbr_parameters(spec))
  def test(self, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile):
    self.init(spec, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile)
    self.encode()

  @slash.parametrize(*gen_av1_vbr_parameters(spec_r2r))
  def test_r2r(self, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile):
    self.init(spec_r2r, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

class cqp_lp(AV1EncoderLPTest):
  def init(self, tspec, case, gop, bframes, tilecols, tilerows,qp, quality, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      case      = case,
      gop       = gop,
      bframes   = bframes,
      qp        = qp,
      rcmode    = "cqp",
      quality   = quality,
      profile   = profile,
      tilerows  = tilerows,
      tilecols  = tilecols,
    )

  @slash.parametrize(*gen_av1_cqp_lp_parameters(spec))
  def test(self, case, gop, bframes, tilecols, tilerows, qp, quality, profile):
    self.init(spec, case, gop, bframes, tilecols, tilerows, qp, quality, profile)
    self.encode()

  @slash.parametrize(*gen_av1_cqp_lp_parameters(spec_r2r))
  def test_r2r(self, case, gop, bframes, tilecols, tilerows, qp, quality, profile):
    self.init(spec_r2r, case, gop, bframes, tilecols, tilerows, qp, quality, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()


class cbr_lp(AV1EncoderLPTest):
  def init(self, tspec, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      gop       = gop,
      maxrate   = bitrate,
      minrate   = bitrate,
      profile   = profile,
      rcmode    = "cbr",
      tilerows  = tilerows,
      tilecols  = tilecols,
      quality   = quality,
      bframes   = bframes,
    )

  @slash.parametrize(*gen_av1_cbr_lp_parameters(spec))
  def test(self, case, gop, bframes, tilecols, tilerows, bitrate, quality, fps, profile):
    self.init(spec, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile)
    self.encode()

  @slash.parametrize(*gen_av1_cbr_lp_parameters(spec_r2r))
  def test_r2r(self, case, gop, bframes, tilecols, tilerows, bitrate, quality, fps, profile):
    self.init(spec_r2r, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()

class vbr_lp(AV1EncoderLPTest):
  def init(self, tspec, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile):
    vars(self).update(tspec[case].copy())
    vars(self).update(
      bitrate   = bitrate,
      case      = case,
      fps       = fps,
      gop       = gop,
      maxrate   = bitrate * 2, # target percentage 50%
      minrate   = bitrate,
      profile   = profile,
      rcmode    = "vbr",
      tilerows  = tilerows,
      tilecols  = tilecols,
      quality   = quality,
      bframes   = bframes,
    )

  @slash.parametrize(*gen_av1_vbr_lp_parameters(spec))
  def test(self, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile):
    self.init(spec, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile)
    self.encode()

  @slash.parametrize(*gen_av1_vbr_lp_parameters(spec_r2r))
  def test_r2r(self, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile):
    self.init(spec_r2r, case, gop, bframes, tilecols, tilerows, bitrate, fps, quality, profile)
    vars(self).setdefault("r2r", 5)
    self.encode()
