from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.core import RuntimeProjectUtil
from com.pnfsoftware.jeb.core.units import IUnit
from com.pnfsoftware.jeb.core.units.code import ICodeUnit
from com.pnfsoftware.jeb.core.units.code.android import IDexUnit

class ShowClassNamesScript(IScript):
    def run(self, ctx):
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

        # 遍历 Dex 单元并显示所有类名
        for dex_unit in dex_units:
            print("Classes in DEX unit: %s" % dex_unit.getName())
            self.show_class_names(dex_unit)

    def show_class_names(self, dex_unit):
        # 获取代码单元
        code_unit = dex_unit.getCodeItem()
        if not isinstance(code_unit, ICodeUnit):
            print("Not a valid code unit")
            return

        # 获取类名列表
        classes = code_unit.getClasses()
        for class_info in classes:
            print("Class Name: %s" % class_info.getName())

# 创建脚本实例并运行
script = ShowClassNamesScript()
script.run(currentState)
