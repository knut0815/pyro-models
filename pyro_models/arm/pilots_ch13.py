# Copyright Contributors to the Pyro project.
# SPDX-License-Identifier: Apache-2.0

# model file: example-models/ARM/Ch.13/pilots.stan
import torch
import pyro
import pyro.distributions as dist

def init_vector(name, dims=None):
    return pyro.sample(name, dist.Normal(torch.zeros(dims), 0.2 * torch.ones(dims)).to_event(1))



def validate_data_def(data):
    assert 'N' in data, 'variable not found in data: key=N'
    assert 'n_groups' in data, 'variable not found in data: key=n_groups'
    assert 'n_scenarios' in data, 'variable not found in data: key=n_scenarios'
    assert 'group_id' in data, 'variable not found in data: key=group_id'
    assert 'scenario_id' in data, 'variable not found in data: key=scenario_id'
    assert 'y' in data, 'variable not found in data: key=y'
    # initialize data
    N = data["N"]
    n_groups = data["n_groups"]
    n_scenarios = data["n_scenarios"]
    group_id = data["group_id"]
    scenario_id = data["scenario_id"]
    y = data["y"]

def init_params(data):
    params = {}
    # initialize data
    N = data["N"]
    n_groups = data["n_groups"]
    n_scenarios = data["n_scenarios"]
    group_id = data["group_id"]
    scenario_id = data["scenario_id"]
    y = data["y"]
    # assign init values for parameters
    params["mu"] = pyro.sample("mu", dist.Uniform(-100., 100.))
    params["sigma_gamma"] = pyro.sample("sigma_gamma", dist.Uniform(0., 100.))
    params["sigma_delta"] = pyro.sample("sigma_delta", dist.Uniform(0., 100.))
    params["sigma_y"] = pyro.sample("sigma_y", dist.Uniform(0., 100.))

    return params

def model(data, params):
    # initialize data
    N = data["N"]
    n_groups = data["n_groups"]
    n_scenarios = data["n_scenarios"]
    group_id = data["group_id"].long() - 1
    scenario_id = data["scenario_id"].long() - 1
    y = data["y"]

    # init parameters
    mu = params["mu"]
    sigma_gamma = params["sigma_gamma"]
    sigma_delta = params["sigma_delta"]
    sigma_y = params["sigma_y"]

    # model block
    with pyro.plate('n_groups', n_groups):
        gamma =  pyro.sample("gamma", dist.Normal(0., sigma_gamma))
    with pyro.plate('n_scenarios', n_scenarios):
        delta =  pyro.sample("delta", dist.Normal(0., sigma_delta))
    with pyro.plate('data', N):
        y_hat = mu + gamma[group_id] + delta[scenario_id]
        y =  pyro.sample("y", dist.Normal(y_hat, sigma_y), obs=y)
