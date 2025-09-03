import math

class EnergyCalculator:
    """
    一个用于计算特定能量公式的类。

    该类强制输入值 x 为非负整数，并提供了计算单个点和
    一定范围内整数点能量值的方法。

    """

    def __init__(self):
        """初始化能量计算器。"""
        # 这个类是无状态的，所以初始化方法不需要做任何事。
        pass

    def calculate(self, x: int) -> float:
        """
        根据新公式(v3)计算单个点的能量值。
        """
        # --- 输入验证 ---
        if not isinstance(x, int) or x < 0:
            raise ValueError("输入值 x 必须是大于等于0的整数。")

        # --- 公式的第一部分 (基础能量) ---
        part1 = 35 + 15 * math.sin(math.sqrt(x))

        # --- 公式的第二部分 (尖峰能量) ---

        # log 系数
        log_coefficient = 2 * math.log(x + 1)

        # 第一个高次幂项
        # 除非 sin(x) 极度接近 1，否则此项几乎为 0
        term_a_base = (math.sin(x) + 1) / 2
        term_a = term_a_base ** 2000

        # 第二个高次幂项 (决定性的尖峰)
        # 如果 x 是偶数，此项为 1；如果是奇数，此项为 0。
        term_b_base = (math.cos(x * math.pi) + 1) / 2
        term_b = term_b_base ** 2200

        # 组合第二部分
        part2 = log_coefficient * (term_a + term_b)

        part3 = 48 + 30 * math.sin(x * 0.3) + 12 * math.cos(x * 0.9) + 5 * math.sin(x * 2.1)

        # --- 公式的第二部分 ---
        # 指数部分 sin((π/1000)*(x-50))^2
        inner_sin_term = math.sin((math.pi / 100000) * (x - 50))
        exponent_term = -3 * (inner_sin_term ** 2)

        # 指数前的系数部分
        coefficient_term = 800 + 150 * math.sin(x * 0.001)

        part4 = coefficient_term * math.exp(exponent_term)

        # --- 最终结果 ---
        return 0.5*(part1 + part2) + 0.1*(part3 + part4)

    def calculate_range(self, start: int, end: int) -> list:
        """
        计算指定闭区间 [start, end] 内所有整数点的能量值。

        Args:
            start (int): 范围的起始值（包含），必须是大于等于0的整数。
            end (int): 范围的结束值（包含），必须是大于等于 start 的整数。

        Returns:
            list: 一个包含 (x, energy) 元组的列表。

        Raises:
            ValueError: 如果 start 或 end 不符合要求。
        """
        # --- 范围验证 ---
        if not isinstance(start, int) or start < 0:
            raise ValueError("起始值 start 必须是大于等于0的整数。")
        if not isinstance(end, int):
            raise ValueError("结束值 end 必须是整数。")
        if start > end:
            raise ValueError("起始值 start 不能大于结束值 end。")

        results = []
        for x in range(start, end + 1):
            energy_value = self.calculate(x)
            results.append((x, energy_value))

        return results


if __name__ == "__main__":

    import matplotlib.pyplot as plt

    # 1. 创建计算器实例
    calculator = EnergyCalculator()

    # 2. 定义要计算和绘制的范围
    x_start = 0
    x_end = 100

    # 3. 计算范围内的所有能量值
    print(f"正在计算从 x={x_start} 到 x={x_end} 的能量值...")
    try:
        # 使用 calculate_range 方法获取 (x, energy) 形式的元组列表
        energy_data = calculator.calculate_range(x_start, x_end)
        print("计算完成。")
    except ValueError as e:
        print(f"计算过程中发生错误: {e}")
        # 如果出错，则退出程序
        exit()

    # 4. 准备绘图数据
    # energy_data 是一个 [(x1, y1), (x2, y2), ...] 格式的列表
    # 我们需要将 x 和 y 分离成两个独立的列表
    # zip(*energy_data) 是一个巧妙的方法，可以实现这个目的
    x_values, y_values = zip(*energy_data)

    # 5. 使用 matplotlib 绘制图形
    print("正在绘制图形...")
    # 创建一个图形，并指定其大小
    plt.figure(figsize=(14, 7))

    # 绘制散点图
    # s 参数控制点的大小
    # label 参数用于图例
    plt.scatter(x_values, y_values, s=15, color='blue', label='Energy(x) 值')

    # (可选) 绘制一条连接线，以更好地观察趋势
    plt.plot(x_values, y_values, color='lightblue', linestyle='--', linewidth=1, alpha=0.7)

    # 6. 添加图形的标题和标签
    plt.title(f'Energy(x) in Range [{x_start}, {x_end}]', fontsize=16)
    plt.xlabel('x (整数)', fontsize=12)
    plt.ylabel('Energy 值', fontsize=12)

    # 添加网格线，使图形更易读
    plt.grid(True, linestyle=':', alpha=0.6)

    # 显示图例
    plt.legend()

    # 7. 显示图形
    print("图形已生成，即将显示。")
    plt.show()