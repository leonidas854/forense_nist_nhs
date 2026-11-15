"""Adaptación local del lanzador GUI de pyghidra-mcp f367da4.

El lanzador upstream omite la ruta del proyecto al iniciar Ghidra. Pasarla
explícitamente evita que se abra el último proyecto de otra investigación.
El guardado incluye los programas, además de los metadatos del proyecto.
"""
from pyghidra_mcp.gui_launcher import GuiPyGhidraMcpLauncher
from pyghidra_mcp.gui_context import GuiPyGhidraContext
from pyghidra_mcp.server import main


original_init = GuiPyGhidraMcpLauncher.__init__


def init_project(self, project_gpr_path, *args, **kwargs):
    original_init(self, project_gpr_path, *args, **kwargs)
    if project_gpr_path.exists():
        self.args = [str(project_gpr_path)]


def save_programs(self):
    from ghidra.util.task import TaskMonitor

    self.refresh_programs()
    with self._programs_lock:
        for info in self.programs.values():
            info.program.save("Guardado pericial mediante MCP", TaskMonitor.DUMMY)
        self.project.save()


GuiPyGhidraMcpLauncher.__init__ = init_project
GuiPyGhidraContext.save = save_programs

if __name__ == "__main__":
    main()
