from .zero_inflated import ZeroAdjustedGamma as ZeroAdjustedGamma_Torch
from xgboostlss.utils import *
from .distribution_utils import *


class ZAGA:
    """
    Zero-Adjusted Gamma distribution class.

    The zero-adjusted Gamma distribution is similar to the Gamma distribution but allows zeros as y values.

     Distributional Parameters
    --------------------------
    concentration: torch.Tensor
        shape parameter of the distribution (often referred to as alpha)
    rate: torch.Tensor
        rate = 1 / scale of the distribution (often referred to as beta)
    gate: torch.Tensor
        Probability of zeros given via a Bernoulli distribution.

    Source
    -------------------------
    - https://github.com/pyro-ppl/pyro/blob/dev/pyro/distributions/zero_inflated.py#L150

    Parameters
    -------------------------
    stabilization: str
        Stabilization method for the Gradient and Hessian. Options are "None", "MAD", "L2".
    response_fn: str
        When a custom objective and metric are provided, XGBoost doesn't know its response and link function. Hence,
        the user is responsible for specifying the transformations. Options are "exp" or "softplus".
    """
    def __init__(self,
                 stabilization: str = "None",
                 response_fn: str = "exp"
                 ):
        # Check Response Function
        if response_fn == "exp":
            response_fn = exp_fn
            inverse_response_fn = log_fn
        elif response_fn == "softplus":
            response_fn = softplus_fn
            inverse_response_fn = softplusinv_fn
        else:
            raise ValueError("Invalid response function. Please choose from 'exp' or 'softplus'.")

        # Specify Response and Link Functions
        param_dict = {"concentration": response_fn, "rate": response_fn, "gate": sigmoid_fn}
        param_dict_inv = {"concentration": inverse_response_fn, "rate": inverse_response_fn, "gate": sigmoidinv_fn}
        distribution_arg_names = list(param_dict.keys())

        # Specify Distribution
        self.dist_class = DistributionClass(distribution=ZeroAdjustedGamma_Torch,
                                            univariate=True,
                                            discrete=False,
                                            n_dist_param=len(param_dict),
                                            stabilization=stabilization,
                                            param_dict=param_dict,
                                            param_dict_inv=param_dict_inv,
                                            distribution_arg_names=distribution_arg_names
                                            )
