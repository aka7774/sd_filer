import launch

if not launch.is_installed("yaml"):
    launch.run_pip("install yaml", desc='Installing yaml')
