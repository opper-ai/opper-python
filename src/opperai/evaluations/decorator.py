from typing import List

from opperai.evaluations._base import Evaluation
from opperai.types import Metric


def evaluator(func=None, **decorator_kwargs):
    """Decorator to create an evaluator function.

    The decorated function should return a list of Metric objects.

    Args:
        func: The function to decorate
        **decorator_kwargs: Default parameters to pass to the function

    Returns:
        A function that can be called with parameters to create metrics
    """
    if func is None:
        # Called with parameters: @evaluator(param=value)
        def decorator(f):
            def evaluator_func(**kwargs):
                # Merge default kwargs with provided kwargs
                combined_kwargs = {**decorator_kwargs, **kwargs}
                return f(**combined_kwargs)

            # Copy the original function name and docstring
            evaluator_func.__name__ = f.__name__
            evaluator_func.__doc__ = f.__doc__
            return evaluator_func

        return decorator

    # Called without parameters: @evaluator
    def evaluator_func(**kwargs):
        return func(**kwargs)

    # Copy the original function name and docstring
    evaluator_func.__name__ = func.__name__
    evaluator_func.__doc__ = func.__doc__
    return evaluator_func


async def process_metrics(metric_group: str, metrics: List[Metric]) -> Evaluation:
    """Process a list of metrics into an Evaluation.

    Args:
        metric_group: Name/group for these metrics
        metrics: List of metrics returned by the evaluator

    Returns:
        Evaluation result
    """
    # Ensure we have a list of metrics
    if not isinstance(metrics, list):
        metrics = [metrics]

    # Just store the metrics with the group name
    eval_metrics = {metric_group: metrics}

    return Evaluation(metrics=eval_metrics)
