import unittest

import numpy as np
import numpy.testing as npt

import thalesians.tsa.distrs as distrs
import thalesians.tsa.numpyutils as npu
import thalesians.tsa.random as rnd
import thalesians.tsa.stats as stats

class TestDistrs(unittest.TestCase):
    def test_wide_sense_distr(self):
        std_wide_sense_1d = distrs.WideSenseDistr(dim=1)
        npt.assert_almost_equal(std_wide_sense_1d.mean, 0.)
        npt.assert_almost_equal(std_wide_sense_1d.cov, 1.)
        npt.assert_almost_equal(std_wide_sense_1d.vol, 1.)
        
        with self.assertRaises(NotImplementedError):
            std_wide_sense_1d.sample()
        
        std_wide_sense_2d = distrs.WideSenseDistr(dim=2)
        npt.assert_almost_equal(std_wide_sense_2d.mean, npu.col_of(2, 0.))
        npt.assert_almost_equal(std_wide_sense_2d.cov, np.eye(2))
        npt.assert_almost_equal(std_wide_sense_2d.vol, np.eye(2))
        
        with self.assertRaises(NotImplementedError):
            std_wide_sense_2d.sample()
        
        sd1=3.; sd2=4.; cor=-.5

        wide_sense_2d = distrs.WideSenseDistr(mean=[1., 2.], cov=stats.make_cov_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(wide_sense_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(wide_sense_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(wide_sense_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])
        
        with self.assertRaises(NotImplementedError):
            wide_sense_2d.sample()

        wide_sense_2d = distrs.WideSenseDistr(mean=[1., 2.], vol=stats.make_vol_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(wide_sense_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(wide_sense_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(wide_sense_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])
        
        with self.assertRaises(NotImplementedError):
            wide_sense_2d.sample()
    
    def test_normal_distr(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)

        std_normal_1d = distrs.NormalDistr(dim=1)
        npt.assert_almost_equal(std_normal_1d.mean, 0.)
        npt.assert_almost_equal(std_normal_1d.cov, 1.)
        npt.assert_almost_equal(std_normal_1d.vol, 1.)
        
        sample = std_normal_1d.sample()
        self.assertEqual(np.shape(sample), (1, 1))
        npt.assert_almost_equal(sample, [[ 0.49671415]])
        
        sample = std_normal_1d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 1))
        npt.assert_almost_equal(sample, [
                [-0.1382643 ],
                [ 0.64768854],
                [ 1.52302986],
                [-0.23415337],
                [-0.23413696],
                [ 1.57921282],
                [ 0.76743473],
                [-0.46947439],
                [ 0.54256004],
                [-0.46341769]])
        
        std_normal_2d = distrs.NormalDistr(dim=2)
        npt.assert_almost_equal(std_normal_2d.mean, npu.col_of(2, 0.))
        npt.assert_almost_equal(std_normal_2d.cov, np.eye(2))
        npt.assert_almost_equal(std_normal_2d.vol, np.eye(2))
        
        sample = std_normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [-0.46572975,  0.24196227],
                [-1.91328024, -1.72491783],
                [-0.56228753, -1.01283112],
                [ 0.31424733, -0.90802408],
                [-1.4123037 ,  1.46564877],
                [-0.2257763 ,  0.0675282 ],
                [-1.42474819, -0.54438272],
                [ 0.11092259, -1.15099358],
                [ 0.37569802, -0.60063869],
                [-0.29169375, -0.60170661]])

        sd1=3.; sd2=4.; cor=-.5

        normal_2d = distrs.NormalDistr(mean=[1., 2.], cov=stats.make_cov_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(normal_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(normal_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(normal_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])

        sample = normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [-3.09581812,  9.06710684],
                [ 5.00400357, -1.07912958],
                [ 4.10821238, -2.42324481],
                [ 2.58989516, -7.05256838],
                [ 2.07671635,  3.61955714],
                [ 0.38728403,  2.5195548 ],
                [-1.36010204, -0.88681309],
                [ 1.63968707, -1.29329703],
                [-0.61960168,  6.44566548],
                [ 5.53451941, -4.36131646]])

        normal_2d = distrs.NormalDistr(mean=[1., 2.], vol=stats.make_vol_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(normal_2d.mean, npu.col(1., 2.))
        npt.assert_almost_equal(normal_2d.cov, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(normal_2d.vol, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])

        sample = normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 0.4624506 , -0.26705979],
                [ 1.76344545,  5.54913479],
                [-2.76038957,  4.57609973],
                [ 2.35608833,  1.20642031],
                [-2.1218454 ,  5.16796697],
                [-0.85307657, -0.00850715],
                [ 5.28771297, -1.62048489],
                [-2.12592264,  7.1016208 ],
                [-0.46508111,  6.26189296],
                [ 3.15543223, -0.04269231]])
        
    def test_dirac_delta_distr(self):
        std_dirac_delta_1d = distrs.DiracDeltaDistr(dim=1)
        npt.assert_almost_equal(std_dirac_delta_1d.mean, 0.)
        npt.assert_almost_equal(std_dirac_delta_1d.cov, 0.)
        npt.assert_almost_equal(std_dirac_delta_1d.vol, 0.)
        
        sample = std_dirac_delta_1d.sample()
        self.assertEqual(np.shape(sample), (1, 1))
        npt.assert_almost_equal(sample, [[ 0. ]])
        
        sample = std_dirac_delta_1d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 1))
        npt.assert_almost_equal(sample, [
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.],
                [ 0.]])
        
        std_dirac_delta_2d = distrs.DiracDeltaDistr(dim=2)
        npt.assert_almost_equal(std_dirac_delta_2d.mean, npu.col_of(2, 0.))
        npt.assert_almost_equal(std_dirac_delta_2d.cov, np.zeros((2, 2)))
        npt.assert_almost_equal(std_dirac_delta_2d.vol, np.zeros((2, 2)))
        
        sample = std_dirac_delta_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.],
                [ 0.,  0.]])

        dirac_delta_2d = distrs.DiracDeltaDistr(mean=[1., 2.], dim=2)
        npt.assert_almost_equal(dirac_delta_2d.mean, [[1.], [2.]])
        npt.assert_almost_equal(dirac_delta_2d.cov, np.zeros((2, 2)))
        npt.assert_almost_equal(dirac_delta_2d.vol, np.zeros((2, 2)))
        
        sample = dirac_delta_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.],
                [ 1.,  2.]])
    
    def test_log_normal_distr(self):
        rnd.random_state(np.random.RandomState(seed=42), force=True)

        std_log_normal_1d = distrs.LogNormalDistr(dim=1)
        npt.assert_almost_equal(std_log_normal_1d.mean, [[ 1.6487213]])
        npt.assert_almost_equal(std_log_normal_1d.cov, [[ 4.6707743]])
        npt.assert_almost_equal(std_log_normal_1d.vol, [[ 2.1611974]])
        
        sample = std_log_normal_1d.sample(size=1)
        self.assertEqual(np.shape(sample), (1, 1))
        npt.assert_almost_equal(sample, [[ 1.6433127]])
        
        sample = std_log_normal_1d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 1))
        npt.assert_almost_equal(sample, [
                [ 0.87086849],
                [ 1.91111824],
                [ 4.58609939],
                [ 0.79124045],
                [ 0.79125344],
                [ 4.85113557],
                [ 2.15423297],
                [ 0.62533086],
                [ 1.72040554],
                [ 0.62912979]])
        
        std_log_normal_2d = distrs.LogNormalDistr(dim=2)
        npt.assert_almost_equal(std_log_normal_2d.mean, [
                [ 1.6487213],
                [ 1.6487213]])
        npt.assert_almost_equal(std_log_normal_2d.cov, [
                [ 4.6707743,  0.       ],
                [ 0.       ,  4.6707743]])
        npt.assert_almost_equal(std_log_normal_2d.vol, [
                [ 2.1611974,  0.       ],
                [ 0.       ,  2.1611974]])
        
        sample = std_log_normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 0.62767689,  1.27374614],
                [ 0.14759544,  0.17818769],
                [ 0.5699039 ,  0.36318929],
                [ 1.36922835,  0.40332037],
                [ 0.2435815 ,  4.33035173],
                [ 0.79789657,  1.06986043],
                [ 0.24056903,  0.58019982],
                [ 1.11730841,  0.31632232],
                [ 1.45600738,  0.54846123],
                [ 0.74699727,  0.54787583]])

        sd1=.4; sd2=.4; cor=-.5

        log_normal_2d = distrs.LogNormalDistr(mean_of_log=[1., 1.3], cov_of_log=stats.make_cov_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(log_normal_2d.mean_of_log, npu.col(1., 1.3))
        npt.assert_almost_equal(log_normal_2d.cov_of_log, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(log_normal_2d.vol_of_log, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])
        npt.assert_almost_equal(log_normal_2d.mean, [[ 2.9446796], [ 3.9749016]])
        npt.assert_almost_equal(log_normal_2d.cov, [[ 1.5045366, -0.8999087], [-0.8999087,  2.7414445]])
        npt.assert_almost_equal(log_normal_2d.vol, [[ 1.2265956,  0.       ], [-0.7336637,  1.484312 ]])

        sample = log_normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 1.42711164,  6.95143797],
                [ 4.62238496,  2.99848502],
                [ 4.32618186,  2.50643161],
                [ 4.10913455,  1.42691268],
                [ 2.94320341,  4.55346303],
                [ 2.50304159,  3.80468825],
                [ 2.24476532,  2.45957906],
                [ 3.18112082,  2.60781028],
                [ 2.01884543,  5.66848303],
                [ 5.34174201,  2.12565878]])

        log_normal_2d = distrs.LogNormalDistr(mean_of_log=[1., 1.3], vol_of_log=stats.make_vol_2d(sd1=sd1, sd2=sd2, cor=cor))
        npt.assert_almost_equal(log_normal_2d.mean_of_log, npu.col(1., 1.3))
        npt.assert_almost_equal(log_normal_2d.cov_of_log, [[sd1*sd1, cor*sd1*sd2], [cor*sd1*sd2, sd2*sd2]])
        npt.assert_almost_equal(log_normal_2d.vol_of_log, [[sd1, 0.], [cor*sd2, np.sqrt(1.-cor*cor)*sd2]])
        npt.assert_almost_equal(log_normal_2d.mean, npu.col(2.9446796, 3.9749016))
        npt.assert_almost_equal(log_normal_2d.cov, [[ 1.5045366, -0.8999087], [-0.8999087,  2.7414445]])
        npt.assert_almost_equal(log_normal_2d.vol, [[ 1.2265956,  0.       ], [-0.7336637,  1.484312 ]])

        sample = log_normal_2d.sample(size=10)
        self.assertEqual(np.shape(sample), (10, 2))
        npt.assert_almost_equal(sample, [
                [ 2.71288329,  2.80448293],
                [ 2.70285608,  5.57387658],
                [ 1.66454464,  4.28346127],
                [ 3.23285936,  3.52238521],
                [ 1.76160691,  4.67441442],
                [ 2.32343609,  2.75776026],
                [ 4.8398479 ,  2.85230385],
                [ 1.67494888,  5.78583855],
                [ 2.06409776,  5.58431178],
                [ 3.6537541 ,  3.15441508]])

if __name__ == '__main__':
    unittest.main()
