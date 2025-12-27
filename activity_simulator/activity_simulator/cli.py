"""
Command-line interface for activity simulator
"""
import click
import sys
import os
import logging
from pathlib import Path
from .config import Config
from .daemon import DaemonController

logger = logging.getLogger(__name__)


@click.group()
@click.option("--config", "-c", type=click.Path(), help="Path to configuration file")
@click.pass_context
def main(ctx, config):
    """Activity Simulator - Windows activity simulator with anti-detection"""
    ctx.ensure_object(dict)
    
    if config and os.path.exists(config):
        ctx.obj["config"] = Config(config)
    else:
        default_config = Path.home() / ".activity_sim" / "config.yaml"
        if default_config.exists():
            ctx.obj["config"] = Config(str(default_config))
        else:
            ctx.obj["config"] = Config()


@main.command()
@click.pass_context
def start(ctx):
    """Start the activity simulator daemon"""
    config = ctx.obj["config"]
    controller = DaemonController(config)
    
    if controller.is_running():
        click.echo("Activity simulator is already running", err=True)
        sys.exit(1)
    
    click.echo("Starting activity simulator...")
    
    try:
        controller.start()
    except KeyboardInterrupt:
        click.echo("\nStopping activity simulator...")
        controller.stop()
    except Exception as e:
        click.echo(f"Failed to start: {e}", err=True)
        sys.exit(1)


@main.command()
@click.pass_context
def stop(ctx):
    """Stop the activity simulator daemon"""
    config = ctx.obj["config"]
    controller = DaemonController(config)
    
    if not controller.is_running():
        click.echo("Activity simulator is not running", err=True)
        sys.exit(1)
    
    click.echo("Stopping activity simulator...")
    if controller.stop():
        click.echo("Activity simulator stopped")
    else:
        click.echo("Failed to stop activity simulator", err=True)
        sys.exit(1)


@main.command()
@click.pass_context
def status(ctx):
    """Check activity simulator status"""
    config = ctx.obj["config"]
    controller = DaemonController(config)
    
    status = controller.status()
    if status["running"]:
        click.echo(f"Activity simulator is running (PID: {status['pid']})")
    else:
        click.echo("Activity simulator is not running")


@main.command()
@click.pass_context
def restart(ctx):
    """Restart the activity simulator daemon"""
    config = ctx.obj["config"]
    controller = DaemonController(config)
    
    if controller.is_running():
        click.echo("Stopping activity simulator...")
        controller.stop()
    
    click.echo("Starting activity simulator...")
    try:
        controller.start()
    except KeyboardInterrupt:
        click.echo("\nStopping activity simulator...")
        controller.stop()
    except Exception as e:
        click.echo(f"Failed to restart: {e}", err=True)
        sys.exit(1)


@main.command()
@click.option("--output", "-o", type=click.Path(), help="Output path for config file")
@click.pass_context
def init_config(ctx, output):
    """Initialize default configuration file"""
    if output is None:
        config_dir = Path.home() / ".activity_sim"
        config_dir.mkdir(exist_ok=True)
        output = config_dir / "config.yaml"
    
    output_path = Path(output)
    if output_path.exists():
        if not click.confirm(f"Config file {output} already exists. Overwrite?"):
            return
    
    config = Config()
    config.save_config(str(output_path))
    click.echo(f"Configuration file created at: {output_path}")


@main.command()
@click.pass_context
def test(ctx):
    """Test input injection (single mouse movement)"""
    from .win32_input import Win32InputInjector
    from .activities import MouseActivity
    
    click.echo("Testing input injection...")
    
    try:
        injector = Win32InputInjector()
        mouse = MouseActivity(injector)
        
        click.echo("Moving mouse to random position...")
        if mouse.random_mouse_movement():
            click.echo("✓ Mouse movement successful")
        else:
            click.echo("✗ Mouse movement failed", err=True)
            
        click.echo("\nScrolling...")
        if mouse.scroll_activity("down"):
            click.echo("✓ Scroll successful")
        else:
            click.echo("✗ Scroll failed", err=True)
            
    except Exception as e:
        click.echo(f"Test failed: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
