"""
This modules provides functionality to create classes with the intention
of mimicking another module or classes API and then invoking a dispatch
function to implement some desired, alternate behaviour.
"""


from .factories import mimic_factory


__all__ = ['mimic_factory']
