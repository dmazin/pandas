from __future__ import division, print_function

from functools import partial

import numpy as np

from pandas.core.common import isnull
import pandas.core.nanops as nanops
import pandas.util.testing as tm

nanops._USE_BOTTLENECK = False


class TestnanopsDataFrame(tm.TestCase):
    def setUp(self):
        self.arr_shape = (11, 7, 5)

        self.arr_float = np.random.randn(*self.arr_shape)
        self.arr_float1 = np.random.randn(*self.arr_shape)
        self.arr_complex = self.arr_float + self.arr_float1*1j
        self.arr_int = np.random.randint(-10, 10, self.arr_shape)
        self.arr_bool = np.random.randint(0, 2, self.arr_shape) == 0
        self.arr_str = np.abs(self.arr_float).astype('S')
        self.arr_utf = np.abs(self.arr_float).astype('U')
        self.arr_date = np.random.randint(0, 20000,
                                          self.arr_shape).astype('M8[ns]')
        self.arr_tdelta = np.random.randint(0, 20000,
                                            self.arr_shape).astype('m8[ns]')

        self.arr_nan = np.tile(np.nan, self.arr_shape)
        self.arr_float_nan = np.vstack([self.arr_float, self.arr_nan])
        self.arr_float1_nan = np.vstack([self.arr_float1, self.arr_nan])
        self.arr_nan_float1 = np.vstack([self.arr_nan, self.arr_float1])
        self.arr_nan_nan = np.vstack([self.arr_nan, self.arr_nan])

        self.arr_inf = self.arr_float*np.inf
        self.arr_float_inf = np.vstack([self.arr_float, self.arr_inf])
        self.arr_float1_inf = np.vstack([self.arr_float1, self.arr_inf])
        self.arr_inf_float1 = np.vstack([self.arr_inf, self.arr_float1])
        self.arr_inf_inf = np.vstack([self.arr_inf, self.arr_inf])

        self.arr_nan_inf = np.vstack([self.arr_nan, self.arr_inf])
        self.arr_float_nan_inf = np.vstack([self.arr_float,
                                            self.arr_nan,
                                            self.arr_inf])
        self.arr_nan_float1_inf = np.vstack([self.arr_float,
                                             self.arr_inf,
                                             self.arr_nan])
        self.arr_nan_nan_inf = np.vstack([self.arr_nan,
                                          self.arr_nan,
                                          self.arr_inf])
        self.arr_obj = np.vstack([self.arr_float.astype('O'),
                                  self.arr_int.astype('O'),
                                  self.arr_bool.astype('O'),
                                  self.arr_complex.astype('O'),
                                  self.arr_str.astype('O'),
                                  self.arr_utf.astype('O'),
                                  self.arr_date.astype('O'),
                                  self.arr_tdelta.astype('O')])

        self.arr_nan_nanj = self.arr_nan + self.arr_nan*1j
        self.arr_complex_nan = np.vstack([self.arr_complex, self.arr_nan_nanj])

        self.arr_nan_infj = self.arr_inf*1j
        self.arr_complex_nan_infj = np.vstack([self.arr_complex,
                                              self.arr_nan_infj])

        self.arr_float_2d = self.arr_float[:, :, 0]
        self.arr_float1_2d = self.arr_float1[:, :, 0]
        self.arr_complex_2d = self.arr_complex[:, :, 0]
        self.arr_int_2d = self.arr_int[:, :, 0]
        self.arr_bool_2d = self.arr_bool[:, :, 0]
        self.arr_str_2d = self.arr_str[:, :, 0]
        self.arr_utf_2d = self.arr_utf[:, :, 0]
        self.arr_date_2d = self.arr_date[:, :, 0]
        self.arr_tdelta_2d = self.arr_tdelta[:, :, 0]

        self.arr_nan_2d = self.arr_nan[:, :, 0]
        self.arr_float_nan_2d = self.arr_float_nan[:, :, 0]
        self.arr_float1_nan_2d = self.arr_float1_nan[:, :, 0]
        self.arr_nan_float1_2d = self.arr_nan_float1[:, :, 0]
        self.arr_nan_nan_2d = self.arr_nan_nan[:, :, 0]
        self.arr_nan_nanj_2d = self.arr_nan_nanj[:, :, 0]
        self.arr_complex_nan_2d = self.arr_complex_nan[:, :, 0]

        self.arr_inf_2d = self.arr_inf[:, :, 0]
        self.arr_float_inf_2d = self.arr_float_inf[:, :, 0]
        self.arr_nan_inf_2d = self.arr_nan_inf[:, :, 0]
        self.arr_float_nan_inf_2d = self.arr_float_nan_inf[:, :, 0]
        self.arr_nan_nan_inf_2d = self.arr_nan_nan_inf[:, :, 0]

        self.arr_float_1d = self.arr_float[:, 0, 0]
        self.arr_float1_1d = self.arr_float1[:, 0, 0]
        self.arr_complex_1d = self.arr_complex[:, 0, 0]
        self.arr_int_1d = self.arr_int[:, 0, 0]
        self.arr_bool_1d = self.arr_bool[:, 0, 0]
        self.arr_str_1d = self.arr_str[:, 0, 0]
        self.arr_utf_1d = self.arr_utf[:, 0, 0]
        self.arr_date_1d = self.arr_date[:, 0, 0]
        self.arr_tdelta_1d = self.arr_tdelta[:, 0, 0]

        self.arr_nan_1d = self.arr_nan[:, 0, 0]
        self.arr_float_nan_1d = self.arr_float_nan[:, 0, 0]
        self.arr_float1_nan_1d = self.arr_float1_nan[:, 0, 0]
        self.arr_nan_float1_1d = self.arr_nan_float1[:, 0, 0]
        self.arr_nan_nan_1d = self.arr_nan_nan[:, 0, 0]
        self.arr_nan_nanj_1d = self.arr_nan_nanj[:, 0, 0]
        self.arr_complex_nan_1d = self.arr_complex_nan[:, 0, 0]

        self.arr_inf_1d = self.arr_inf.ravel()
        self.arr_float_inf_1d = self.arr_float_inf[:, 0, 0]
        self.arr_nan_inf_1d = self.arr_nan_inf[:, 0, 0]
        self.arr_float_nan_inf_1d = self.arr_float_nan_inf[:, 0, 0]
        self.arr_nan_nan_inf_1d = self.arr_nan_nan_inf[:, 0, 0]

    def check_results(self, targ, res, axis):
        res = getattr(res, 'asm8', res)
        res = getattr(res, 'values', res)
        if axis != 0 and hasattr(targ, 'shape') and targ.ndim:
            res = np.split(res, [targ.shape[0]], axis=0)[0]
        tm.assert_almost_equal(targ, res)

    def check_fun_data(self, testfunc, targfunc,
                       testarval, targarval, targarnanval, **kwargs):
        for axis in list(range(targarval.ndim)):
            for skipna in [False, True]:
                targartempval = targarval if skipna else targarnanval
                try:
                    targ = targfunc(targartempval, axis=axis, **kwargs)
                    res = testfunc(testarval, axis=axis, skipna=skipna,
                                   **kwargs)
                    self.check_results(targ, res, axis)
                    if skipna:
                        res = testfunc(testarval, axis=axis)
                        self.check_results(targ, res, axis)
                    if axis is None:
                        res = testfunc(testarval, skipna=skipna)
                        self.check_results(targ, res, axis)
                    if skipna and axis is None:
                        res = testfunc(testarval)
                        self.check_results(targ, res, axis)
                except BaseException as exc:
                    exc.args += ('axis: %s of %s' % (axis, testarval.ndim-1),
                                 'skipna: %s' % skipna,
                                 'kwargs: %s' % kwargs)
                    raise

        if testarval.ndim <= 1:
            return

        try:
            testarval2 = np.take(testarval, 0, axis=-1)
            targarval2 = np.take(targarval, 0, axis=-1)
            targarnanval2 = np.take(targarnanval, 0, axis=-1)
        except ValueError:
            return
        self.check_fun_data(testfunc, targfunc,
                            testarval2, targarval2, targarnanval2,
                            **kwargs)

    def check_fun(self, testfunc, targfunc,
                  testar, targar=None, targarnan=None,
                  **kwargs):
        if targar is None:
            targar = testar
        if targarnan is None:
            targarnan = testar
        testarval = getattr(self, testar)
        targarval = getattr(self, targar)
        targarnanval = getattr(self, targarnan)
        try:
            self.check_fun_data(testfunc, targfunc,
                                testarval, targarval, targarnanval, **kwargs)
        except BaseException as exc:
            exc.args += ('testar: %s' % testar,
                         'targar: %s' % targar,
                         'targarnan: %s' % targarnan)
            raise

    def check_funs(self, testfunc, targfunc,
                   allow_complex=True, allow_all_nan=True, allow_str=True,
                   allow_date=True, allow_obj=True,
                   **kwargs):
        self.check_fun(testfunc, targfunc, 'arr_float', **kwargs)
        self.check_fun(testfunc, targfunc, 'arr_float_nan', 'arr_float',
                       **kwargs)
        self.check_fun(testfunc, targfunc, 'arr_int', **kwargs)
        self.check_fun(testfunc, targfunc, 'arr_bool', **kwargs)
        objs = [self.arr_float.astype('O'),
                self.arr_int.astype('O'),
                self.arr_bool.astype('O')]

        if allow_all_nan:
            self.check_fun(testfunc, targfunc, 'arr_nan', **kwargs)

        if allow_complex:
            self.check_fun(testfunc, targfunc, 'arr_complex', **kwargs)
            self.check_fun(testfunc, targfunc,
                           'arr_complex_nan', 'arr_complex', **kwargs)
            if allow_all_nan:
                self.check_fun(testfunc, targfunc, 'arr_nan_nanj', **kwargs)
            objs += [self.arr_complex.astype('O')]

        if allow_str:
            self.check_fun(testfunc, targfunc, 'arr_str', **kwargs)
            self.check_fun(testfunc, targfunc, 'arr_utf', **kwargs)
            objs += [self.arr_str.astype('O'),
                     self.arr_utf.astype('O')]

        if allow_date:
            self.check_fun(testfunc, targfunc, 'arr_date', **kwargs)
            self.check_fun(testfunc, targfunc, 'arr_tdelta', **kwargs)
            objs += [self.arr_date.astype('O'),
                     self.arr_tdelta.astype('O')]

        if allow_obj:
            self.arr_obj = np.vstack(objs)
            self.check_fun(testfunc, targfunc, 'arr_obj', **kwargs)

    def check_funs_ddof(self, testfunc, targfunc,
                        allow_complex=True, allow_all_nan=True, allow_str=True,
                        allow_date=True, allow_obj=True,):
        for ddof in range(3):
            try:
                self.check_funs(self, testfunc, targfunc,
                                allow_complex, allow_all_nan, allow_str,
                                allow_date, allow_obj,
                                ddof=ddof)
            except BaseException as exc:
                exc.args += ('ddof %s' % ddof,)

    def test_nanany(self):
        self.check_funs(nanops.nanany, np.any,
                        allow_all_nan=False, allow_str=False, allow_date=False)

    def test_nanall(self):
        self.check_funs(nanops.nanall, np.all,
                        allow_all_nan=False, allow_str=False, allow_date=False)

    def test_nansum(self):
        self.check_funs(nanops.nansum, np.sum,
                        allow_str=False, allow_date=False)

    def _nanmean_wrap(self, value, *args, **kwargs):
        dtype = value.dtype
        res = nanops.nanmean(value, *args, **kwargs)
        if dtype.kind == 'O':
            res = np.round(res, decimals=13)
        return res

    def _mean_wrap(self, value, *args, **kwargs):
        dtype = value.dtype
        if dtype.kind == 'O':
            value = value.astype('c16')
        res = np.mean(value, *args, **kwargs)
        if dtype.kind == 'O':
            res = np.round(res, decimals=13)
        return res

    def test_nanmean(self):
        self.check_funs(self._nanmean_wrap, self._mean_wrap,
                        allow_complex=False, allow_obj=False,
                        allow_str=False, allow_date=False)

    def _median_wrap(self, value, *args, **kwargs):
        if value.dtype.kind == 'O':
            value = value.astype('c16')
        res = np.median(value, *args, **kwargs)
        return res

    def test_nanmedian(self):
        self.check_funs(nanops.nanmedian, self._median_wrap,
                        allow_complex=False, allow_str=False, allow_date=False)

    def test_nanvar(self):
        self.check_funs_ddof(nanops.nanvar, np.var,
                             allow_complex=False, allow_date=False)

    def test_nansem(self):
        tm.skip_if_no_package('scipy.stats')
        self.check_funs_ddof(nanops.nansem, np.var,
                             allow_complex=False, allow_date=False)

    def _minmax_wrap(self, value, axis=None, func=None):
        res = func(value, axis)
        if res.dtype.kind == 'm':
            res = np.atleast_1d(res)
        return res

    def test_nanmin(self):
        func = partial(self._minmax_wrap, func=np.min)
        self.check_funs(nanops.nanmin, func,
                        allow_str=False, allow_obj=False)

    def test_nanmax(self):
        func = partial(self._minmax_wrap, func=np.max)
        self.check_funs(nanops.nanmax, func,
                        allow_str=False, allow_obj=False)

    def _argminmax_wrap(self, value, axis=None, func=None):
        res = func(value, axis)
        nans = np.min(value, axis)
        nullnan = isnull(nans)
        if res.ndim:
            res[nullnan] = -1
        elif (hasattr(nullnan, 'all') and nullnan.all() or
              not hasattr(nullnan, 'all') and nullnan):
            res = -1
        return res

    def test_nanargmax(self):
        func = partial(self._argminmax_wrap, func=np.argmax)
        self.check_funs(nanops.nanargmax, func,
                        allow_str=False, allow_obj=False)

    def test_nanargmin(self):
        func = partial(self._argminmax_wrap, func=np.argmin)
        if tm.sys.version_info[0:2] == (2, 6):
            self.check_funs(nanops.nanargmin, func,
                            allow_date=False,
                            allow_str=False, allow_obj=False)
        else:
            self.check_funs(nanops.nanargmin, func,
                            allow_str=False, allow_obj=False)

    def _skew_kurt_wrap(self, values, axis=None, func=None):
        if not isinstance(values.dtype.type, np.floating):
            values = values.astype('f8')
        result = func(values, axis=axis, bias=False)
        # fix for handling cases where all elements in an axis are the same
        if isinstance(result, np.ndarray):
            result[np.max(values, axis=axis) == np.min(values, axis=axis)] = 0
            return result
        elif np.max(values) == np.min(values):
            return 0.
        return result

    def test_nanskew(self):
        tm.skip_if_no_package('scipy.stats')
        from scipy.stats import skew
        func = partial(self._skew_kurt_wrap, func=skew)
        self.check_funs(nanops.nanskew, func,
                        allow_complex=False, allow_str=False, allow_date=False)

    def test_nankurt(self):
        tm.skip_if_no_package('scipy.stats')
        from scipy.stats import kurtosis
        func1 = partial(kurtosis, fisher=True)
        func = partial(self._skew_kurt_wrap, func=func1)
        self.check_funs(nanops.nankurt, func,
                        allow_complex=False, allow_str=False, allow_date=False)

    def test_nanprod(self):
        self.check_funs(nanops.nanprod, np.prod,
                        allow_str=False, allow_date=False)

    def check_nancorr_nancov_2d(self, checkfun, targ0, targ1, **kwargs):
        res00 = checkfun(self.arr_float_2d, self.arr_float1_2d,
                         **kwargs)
        res01 = checkfun(self.arr_float_2d, self.arr_float1_2d,
                         min_periods=len(self.arr_float_2d)-1,
                         **kwargs)
        tm.assert_almost_equal(targ0, res00)
        tm.assert_almost_equal(targ0, res01)

        res10 = checkfun(self.arr_float_nan_2d, self.arr_float1_nan_2d,
                         **kwargs)
        res11 = checkfun(self.arr_float_nan_2d, self.arr_float1_nan_2d,
                         min_periods=len(self.arr_float_2d)-1,
                         **kwargs)
        tm.assert_almost_equal(targ1, res10)
        tm.assert_almost_equal(targ1, res11)

        targ2 = np.nan
        res20 = checkfun(self.arr_nan_2d, self.arr_float1_2d,
                         **kwargs)
        res21 = checkfun(self.arr_float_2d, self.arr_nan_2d,
                         **kwargs)
        res22 = checkfun(self.arr_nan_2d, self.arr_nan_2d,
                         **kwargs)
        res23 = checkfun(self.arr_float_nan_2d, self.arr_nan_float1_2d,
                         **kwargs)
        res24 = checkfun(self.arr_float_nan_2d, self.arr_nan_float1_2d,
                         min_periods=len(self.arr_float_2d)-1,
                         **kwargs)
        res25 = checkfun(self.arr_float_2d, self.arr_float1_2d,
                         min_periods=len(self.arr_float_2d)+1,
                         **kwargs)
        tm.assert_almost_equal(targ2, res20)
        tm.assert_almost_equal(targ2, res21)
        tm.assert_almost_equal(targ2, res22)
        tm.assert_almost_equal(targ2, res23)
        tm.assert_almost_equal(targ2, res24)
        tm.assert_almost_equal(targ2, res25)

    def check_nancorr_nancov_1d(self, checkfun, targ0, targ1, **kwargs):
        res00 = checkfun(self.arr_float_1d, self.arr_float1_1d,
                         **kwargs)
        res01 = checkfun(self.arr_float_1d, self.arr_float1_1d,
                         min_periods=len(self.arr_float_1d)-1,
                         **kwargs)
        tm.assert_almost_equal(targ0, res00)
        tm.assert_almost_equal(targ0, res01)

        res10 = checkfun(self.arr_float_nan_1d,
                         self.arr_float1_nan_1d,
                         **kwargs)
        res11 = checkfun(self.arr_float_nan_1d,
                         self.arr_float1_nan_1d,
                         min_periods=len(self.arr_float_1d)-1,
                         **kwargs)
        tm.assert_almost_equal(targ1, res10)
        tm.assert_almost_equal(targ1, res11)

        targ2 = np.nan
        res20 = checkfun(self.arr_nan_1d, self.arr_float1_1d,
                         **kwargs)
        res21 = checkfun(self.arr_float_1d, self.arr_nan_1d,
                         **kwargs)
        res22 = checkfun(self.arr_nan_1d, self.arr_nan_1d,
                         **kwargs)
        res23 = checkfun(self.arr_float_nan_1d,
                         self.arr_nan_float1_1d,
                         **kwargs)
        res24 = checkfun(self.arr_float_nan_1d,
                         self.arr_nan_float1_1d,
                         min_periods=len(self.arr_float_1d)-1,
                         **kwargs)
        res25 = checkfun(self.arr_float_1d,
                         self.arr_float1_1d,
                         min_periods=len(self.arr_float_1d)+1,
                         **kwargs)
        tm.assert_almost_equal(targ2, res20)
        tm.assert_almost_equal(targ2, res21)
        tm.assert_almost_equal(targ2, res22)
        tm.assert_almost_equal(targ2, res23)
        tm.assert_almost_equal(targ2, res24)
        tm.assert_almost_equal(targ2, res25)

    def test_nancorr(self):
        targ0 = np.corrcoef(self.arr_float_2d, self.arr_float1_2d)[0, 1]
        targ1 = np.corrcoef(self.arr_float_2d.flat,
                            self.arr_float1_2d.flat)[0, 1]
        self.check_nancorr_nancov_2d(nanops.nancorr, targ0, targ1)
        targ0 = np.corrcoef(self.arr_float_1d, self.arr_float1_1d)[0, 1]
        targ1 = np.corrcoef(self.arr_float_1d.flat,
                            self.arr_float1_1d.flat)[0, 1]
        self.check_nancorr_nancov_1d(nanops.nancorr, targ0, targ1,
                                     method='pearson')

    def test_nancorr_pearson(self):
        targ0 = np.corrcoef(self.arr_float_2d, self.arr_float1_2d)[0, 1]
        targ1 = np.corrcoef(self.arr_float_2d.flat,
                            self.arr_float1_2d.flat)[0, 1]
        self.check_nancorr_nancov_2d(nanops.nancorr, targ0, targ1,
                                     method='pearson')
        targ0 = np.corrcoef(self.arr_float_1d, self.arr_float1_1d)[0, 1]
        targ1 = np.corrcoef(self.arr_float_1d.flat,
                            self.arr_float1_1d.flat)[0, 1]
        self.check_nancorr_nancov_1d(nanops.nancorr, targ0, targ1,
                                     method='pearson')

    def test_nancorr_kendall(self):
        tm.skip_if_no_package('scipy.stats')
        from scipy.stats import kendalltau
        targ0 = kendalltau(self.arr_float_2d, self.arr_float1_2d)[0]
        targ1 = kendalltau(self.arr_float_2d.flat, self.arr_float1_2d.flat)[0]
        self.check_nancorr_nancov_2d(nanops.nancorr, targ0, targ1,
                                     method='kendall')
        targ0 = kendalltau(self.arr_float_1d, self.arr_float1_1d)[0]
        targ1 = kendalltau(self.arr_float_1d.flat, self.arr_float1_1d.flat)[0]
        self.check_nancorr_nancov_1d(nanops.nancorr, targ0, targ1,
                                     method='kendall')

    def test_nancorr_spearman(self):
        tm.skip_if_no_package('scipy.stats')
        from scipy.stats import spearmanr
        targ0 = spearmanr(self.arr_float_2d, self.arr_float1_2d)[0]
        targ1 = spearmanr(self.arr_float_2d.flat, self.arr_float1_2d.flat)[0]
        self.check_nancorr_nancov_2d(nanops.nancorr, targ0, targ1,
                                     method='spearman')
        targ0 = spearmanr(self.arr_float_1d, self.arr_float1_1d)[0]
        targ1 = spearmanr(self.arr_float_1d.flat, self.arr_float1_1d.flat)[0]
        self.check_nancorr_nancov_1d(nanops.nancorr, targ0, targ1,
                                     method='spearman')

    def test_nancov(self):
        targ0 = np.cov(self.arr_float_2d, self.arr_float1_2d)[0, 1]
        targ1 = np.cov(self.arr_float_2d.flat, self.arr_float1_2d.flat)[0, 1]
        self.check_nancorr_nancov_2d(nanops.nancov, targ0, targ1)
        targ0 = np.cov(self.arr_float_1d, self.arr_float1_1d)[0, 1]
        targ1 = np.cov(self.arr_float_1d.flat, self.arr_float1_1d.flat)[0, 1]
        self.check_nancorr_nancov_1d(nanops.nancov, targ0, targ1)

    def check_nancomp(self, checkfun, targ0):
        arr_float = self.arr_float
        arr_float1 = self.arr_float1
        arr_nan = self.arr_nan
        arr_nan_nan = self.arr_nan_nan
        arr_float_nan = self.arr_float_nan
        arr_float1_nan = self.arr_float1_nan
        arr_nan_float1 = self.arr_nan_float1

        while targ0.ndim:
            try:
                res0 = checkfun(arr_float, arr_float1)
                tm.assert_almost_equal(targ0, res0)

                if targ0.ndim > 1:
                    targ1 = np.vstack([targ0, arr_nan])
                else:
                    targ1 = np.hstack([targ0, arr_nan])
                res1 = checkfun(arr_float_nan, arr_float1_nan)
                tm.assert_almost_equal(targ1, res1)

                targ2 = arr_nan_nan
                res2 = checkfun(arr_float_nan, arr_nan_float1)
                tm.assert_almost_equal(targ2, res2)
            except Exception as exc:
                exc.args += ('ndim: %s' % arr_float.ndim,)
                raise

            try:
                arr_float = np.take(arr_float, 0, axis=-1)
                arr_float1 = np.take(arr_float1, 0, axis=-1)
                arr_nan = np.take(arr_nan, 0, axis=-1)
                arr_nan_nan = np.take(arr_nan_nan, 0, axis=-1)
                arr_float_nan = np.take(arr_float_nan, 0, axis=-1)
                arr_float1_nan = np.take(arr_float1_nan, 0, axis=-1)
                arr_nan_float1 = np.take(arr_nan_float1, 0, axis=-1)
                targ0 = np.take(targ0, 0, axis=-1)
            except ValueError:
                break

    def test_nangt(self):
        targ0 = self.arr_float > self.arr_float1
        self.check_nancomp(nanops.nangt, targ0)

    def test_nange(self):
        targ0 = self.arr_float >= self.arr_float1
        self.check_nancomp(nanops.nange, targ0)

    def test_nanlt(self):
        targ0 = self.arr_float < self.arr_float1
        self.check_nancomp(nanops.nanlt, targ0)

    def test_nanle(self):
        targ0 = self.arr_float <= self.arr_float1
        self.check_nancomp(nanops.nanle, targ0)

    def test_naneq(self):
        targ0 = self.arr_float == self.arr_float1
        self.check_nancomp(nanops.naneq, targ0)

    def test_nanne(self):
        targ0 = self.arr_float != self.arr_float1
        self.check_nancomp(nanops.nanne, targ0)

    def check_bool(self, func, value, correct, *args, **kwargs):
        while getattr(value, 'ndim', True):
            try:
                res0 = func(value, *args, **kwargs)
                if correct:
                    self.assertTrue(res0)
                else:
                    self.assertFalse(res0)
            except BaseException as exc:
                exc.args += ('dim: %s' % getattr(value, 'ndim', value),)
                raise
            if not hasattr(value, 'ndim'):
                break
            try:
                value = np.take(value, 0, axis=-1)
            except ValueError:
                break

    def test__has_infs(self):
        pairs = [('arr_complex_1d', False),
                 ('arr_int_1d', False),
                 ('arr_bool_1d', False),
                 ('arr_str_1d', False),
                 ('arr_utf_1d', False),
                 ('arr_complex_1d', False),
                 ('arr_complex_nan_1d', False),

                 ('arr_nan_nanj_1d', False)]
        pairs_float = [('arr_float_1d', False),
                       ('arr_nan_1d', False),
                       ('arr_float_nan_1d', False),
                       ('arr_nan_nan_1d', False),

                       ('arr_float_inf_1d', True),
                       ('arr_inf_1d', True),
                       ('arr_nan_inf_1d', True),
                       ('arr_float_nan_inf_1d', True),
                       ('arr_nan_nan_inf_1d', True)]

        for arr, correct in pairs:
            val = getattr(self, arr)
            try:
                self.check_bool(nanops._has_infs, val, correct)
            except BaseException as exc:
                exc.args += (arr,)
                raise

        for arr, correct in pairs_float:
            val = getattr(self, arr)
            try:
                self.check_bool(nanops._has_infs, val, correct)
                self.check_bool(nanops._has_infs, val.astype('f4'), correct)
            except BaseException as exc:
                exc.args += (arr,)
                raise

    def test__isfinite(self):
        pairs = [('arr_complex', False),
                 ('arr_int', False),
                 ('arr_bool', False),
                 ('arr_str', False),
                 ('arr_utf', False),
                 ('arr_complex', False),
                 ('arr_complex_nan', True),

                 ('arr_nan_nanj', True),
                 ('arr_nan_infj', True),
                 ('arr_complex_nan_infj', True)]
        pairs_float = [('arr_float', False),
                       ('arr_nan', True),
                       ('arr_float_nan', True),
                       ('arr_nan_nan', True),

                       ('arr_float_inf', True),
                       ('arr_inf', True),
                       ('arr_nan_inf', True),
                       ('arr_float_nan_inf', True),
                       ('arr_nan_nan_inf', True)]

        func1 = lambda x: np.any(nanops._isfinite(x).ravel())
        func2 = lambda x: np.any(nanops._isfinite(x).values.ravel())
        for arr, correct in pairs:
            val = getattr(self, arr)
            try:
                self.check_bool(func1, val, correct)
            except BaseException as exc:
                exc.args += (arr,)
                raise

        for arr, correct in pairs_float:
            val = getattr(self, arr)
            try:
                self.check_bool(func1, val, correct)
                self.check_bool(func1, val.astype('f4'), correct)
                self.check_bool(func1, val.astype('f2'), correct)
            except BaseException as exc:
                exc.args += (arr,)
                raise

    def test__bn_ok_dtype(self):
        self.assertTrue(nanops._bn_ok_dtype(self.arr_float.dtype, 'test'))
        self.assertTrue(nanops._bn_ok_dtype(self.arr_complex.dtype, 'test'))
        self.assertTrue(nanops._bn_ok_dtype(self.arr_int.dtype, 'test'))
        self.assertTrue(nanops._bn_ok_dtype(self.arr_bool.dtype, 'test'))
        self.assertTrue(nanops._bn_ok_dtype(self.arr_str.dtype, 'test'))
        self.assertTrue(nanops._bn_ok_dtype(self.arr_utf.dtype, 'test'))
        self.assertFalse(nanops._bn_ok_dtype(self.arr_date.dtype, 'test'))
        self.assertFalse(nanops._bn_ok_dtype(self.arr_tdelta.dtype, 'test'))
        self.assertFalse(nanops._bn_ok_dtype(self.arr_obj.dtype, 'test'))


class TestEnsureNumeric(tm.TestCase):
    def test_numeric_values(self):
        # Test integer
        self.assertEqual(nanops._ensure_numeric(1), 1, 'Failed for int')
        # Test float
        self.assertEqual(nanops._ensure_numeric(1.1), 1.1, 'Failed for float')
        # Test complex
        self.assertEqual(nanops._ensure_numeric(1 + 2j), 1 + 2j,
                         'Failed for complex')

    def test_ndarray(self):
        # Test numeric ndarray
        values = np.array([1, 2, 3])
        self.assertTrue(np.allclose(nanops._ensure_numeric(values), values),
                        'Failed for numeric ndarray')

        # Test object ndarray
        o_values = values.astype(object)
        self.assertTrue(np.allclose(nanops._ensure_numeric(o_values), values),
                        'Failed for object ndarray')

        # Test convertible string ndarray
        s_values = np.array(['1', '2', '3'], dtype=object)
        self.assertTrue(np.allclose(nanops._ensure_numeric(s_values), values),
                        'Failed for convertible string ndarray')

        # Test non-convertible string ndarray
        s_values = np.array(['foo', 'bar', 'baz'], dtype=object)
        self.assertRaises(ValueError,
                          lambda: nanops._ensure_numeric(s_values))

    def test_convertable_values(self):
        self.assertTrue(np.allclose(nanops._ensure_numeric('1'), 1.0),
                        'Failed for convertible integer string')
        self.assertTrue(np.allclose(nanops._ensure_numeric('1.1'), 1.1),
                        'Failed for convertible float string')
        self.assertTrue(np.allclose(nanops._ensure_numeric('1+1j'), 1 + 1j),
                        'Failed for convertible complex string')

    def test_non_convertable_values(self):
        self.assertRaises(TypeError,
                          lambda: nanops._ensure_numeric('foo'))
        self.assertRaises(TypeError,
                          lambda: nanops._ensure_numeric({}))
        self.assertRaises(TypeError,
                          lambda: nanops._ensure_numeric([]))


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=[__file__, '-vvs', '-x', '--pdb', '--pdb-failure',
                         '-s'], exit=False)
