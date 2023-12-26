from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.client.api import IGraphicalClientContext
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.units import IUnit
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit
from org.eclipse.swt import SWT
from org.eclipse.swt.layout import GridLayout
from org.eclipse.swt.widgets import Display, Shell, Text

class ShowClassNamesPlugin(IScript):
    def run(self, ctx):
        # 获取当前 JEB 客户端上下文
        clientContext = ctx.getGraphicalClientContext()
        if not isinstance(clientContext, IGraphicalClientContext):
            print("This script requires a graphical client context.")
            return

        # 获取当前活动的 JEB 项目
        prj = ctx.getMainProject()
        if prj is None:
            print("No active project")
            return

        # 获取 Dex 单元
        dex_units = RuntimeProjectUtil.findUnitsByType(prj, IDexUnit, False)
        if not dex_units:
            print("No DEX units found")
            return

        # 获取所有类名
        class_names = []
        for dex_unit in dex_units:
            code_unit = dex_unit.getCodeItem()
            if isinstance(code_unit, IUnit):
                classes = code_unit.getClasses()
                for class_info in classes:
                    class_names.append(class_info.getName())

        # 创建显示对象
        display = Display()

        # 创建 shell（窗口）
        shell = Shell(display, SWT.SHELL_TRIM | SWT.BORDER)
        shell.setLayout(GridLayout())
        shell.setText("JEB Class Names")

        # 在 shell 中添加文本框，显示所有类名
        text = Text(shell, SWT.MULTI | SWT.BORDER | SWT.V_SCROLL | SWT.H_SCROLL)
        for class_name in class_names:
            text.append(class_name + "\n")

        # 打开 shell
        shell.open()

        # 运行直到 shell 关闭
        while not shell.isDisposed():
            if not display.readAndDispatch():
                display.sleep()

        # 释放资源
        display.dispose()

# 创建脚本实例并运行
script = ShowClassNamesPlugin()
script.run(currentState)
