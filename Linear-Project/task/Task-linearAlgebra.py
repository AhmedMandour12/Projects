import tkinter as tk
from tkinter import messagebox
from fractions import Fraction

class AdvancedGaussSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Matrix Solver")
        self.root.geometry("850x700")
        
        # المتغيرات الأساسية
        self.matrix_entries = []
        self.rows_var = tk.IntVar(value=3)
        self.cols_var = tk.IntVar(value=3)
        self.eq_var = tk.IntVar(value=3)
        self.method_var = tk.StringVar(value="gaussian")

        self.create_widgets()

    def create_widgets(self):
        # --- العنوان ---
        tk.Label(self.root, text="Matrix Linear Solver", font=("Arial", 16, "bold")).pack(pady=10)

        # --- منطقة التحكم ---
        control_frame = tk.LabelFrame(self.root, text="Settings", padx=10, pady=10)
        control_frame.pack(fill="x", padx=10, pady=5)

        # 1. اختيار الطريقة
        method_frame = tk.Frame(control_frame)
        method_frame.pack(anchor="w", pady=5)
        tk.Label(method_frame, text="Method:", font=("Arial", 10, "bold")).pack(side="left")
        
        tk.Radiobutton(method_frame, text="Gaussian Elimination", 
                       variable=self.method_var, value="gaussian").pack(side="left", padx=10)
        tk.Radiobutton(method_frame, text="Gauss-Jordan", 
                       variable=self.method_var, value="jordan").pack(side="left", padx=10)

        # 2. أبعاد المصفوفة والمعادلات
        dim_frame = tk.Frame(control_frame)
        dim_frame.pack(anchor="w", pady=15)
        
        # خانة عدد الصفوف (Rows)
        tk.Label(dim_frame, text="Rows:", font=("Arial", 10, "bold")).pack(side="left")
        tk.Entry(dim_frame, textvariable=self.rows_var, width=5, justify="center").pack(side="left", padx=5)
        
        # خانة عدد الأعمدة (Columns)
        tk.Label(dim_frame, text="Columns:", font=("Arial", 10, "bold")).pack(side="left", padx=(15, 0))
        tk.Entry(dim_frame, textvariable=self.cols_var, width=5, justify="center").pack(side="left", padx=5)

        # خانة عدد المعادلات (Equations)
        tk.Label(dim_frame, text="Equations:", font=("Arial", 10, "bold")).pack(side="left", padx=(15, 0))
        tk.Entry(dim_frame, textvariable=self.eq_var, width=5, justify="center").pack(side="left", padx=5)

        # زر التوليد
        tk.Button(control_frame, text="Create Matrix", command=self.generate_matrix_grid).pack(pady=5)

        # --- منطقة المصفوفة ---
        self.matrix_canvas_frame = tk.LabelFrame(self.root, text="Matrix Input", padx=5, pady=5)
        self.matrix_canvas_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.canvas = tk.Canvas(self.matrix_canvas_frame)
        self.scrollbar_y = tk.Scrollbar(self.matrix_canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.matrix_canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")

        # --- زر الحل ---
        self.solve_btn = tk.Button(self.root, text="Solve", command=self.solve_system, 
                                   font=("Arial", 12, "bold"), bg="#dddddd")
        self.solve_btn.pack(pady=10)

    def generate_matrix_grid(self):
        # مسح القديم
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.matrix_entries = []

        try:
            rows = self.rows_var.get()
            cols = self.cols_var.get()
        except:
            messagebox.showerror("Error", "Enter valid numbers")
            return

        # --- التعديل المطلوب: إذا كانت المصفوفة غير مربعة، اظهر النتيجة وتوقف ---
        if rows != cols:
            result_window = tk.Toplevel(self.root)
            result_window.title("Result")
            result_window.geometry("400x200")
            
            # عرض النتيجة المطلوبة في منتصف النافذة
            tk.Label(result_window, text="Infinite Solutions", 
                    font=("Arial", 16, "bold"), fg="purple").pack(expand=True)
            
            # الخروج من الدالة فوراً لعدم إظهار الشبكة أو أي شيء آخر
            return 
        # ---------------------------------------------------------------------

        # العناوين (Columns)
        for j in range(cols):
            tk.Label(self.scrollable_frame, text=f"Col {j+1}", font=("Arial", 9, "bold")).grid(row=0, column=j, padx=2)
        
        tk.Label(self.scrollable_frame, text="=", font=("Arial", 10, "bold")).grid(row=0, column=cols, padx=5)
        tk.Label(self.scrollable_frame, text="Result", font=("Arial", 9, "bold")).grid(row=0, column=cols+1, padx=2)

        # المدخلات
        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = tk.Entry(self.scrollable_frame, width=8, justify="center")
                entry.grid(row=i+1, column=j, padx=2, pady=5)
                row_entries.append(entry)
            
            tk.Label(self.scrollable_frame, text="=").grid(row=i+1, column=cols)
            
            b_entry = tk.Entry(self.scrollable_frame, width=8, justify="center")
            b_entry.grid(row=i+1, column=cols+1, padx=2, pady=5)
            row_entries.append(b_entry) 
            
            self.matrix_entries.append(row_entries)

    def get_fraction_matrix(self):
        matrix = []
        try:
            for row_entries in self.matrix_entries:
                row_values = []
                for entry in row_entries:
                    text = entry.get().strip()
                    if not text: text = "0"
                    val = Fraction(text).limit_denominator()
                    row_values.append(val)
                matrix.append(row_values)
            return matrix
        except ValueError:
            return None

    def solve_system(self):
        matrix = self.get_fraction_matrix()
        # إضافة حماية في حالة الضغط على حل والمصفوفة فارغة
        if not matrix:
            messagebox.showerror("Error", "Please create and fill the matrix first!")
            return

        rows = len(matrix)
        cols = len(matrix[0]) - 1 # Last column is 'b'
        method = self.method_var.get()
        
        result_window = tk.Toplevel(self.root)
        result_window.title("Solution")
        result_window.geometry("700x600")
        
        text_area = tk.Text(result_window, font=("Courier", 10), padx=10, pady=10)
        scrollbar = tk.Scrollbar(result_window, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        text_area.pack(side="left", fill="both", expand=True)

        text_area.tag_configure("header", font=("Arial", 11, "bold"), foreground="blue")
        text_area.tag_configure("arabic_step", font=("Arial", 12), foreground="green", justify='right')
        text_area.tag_configure("final", font=("Arial", 12, "bold"), foreground="purple")
        text_area.tag_configure("warning", foreground="#e67e22")
        text_area.tag_configure("error", foreground="red")

        text_area.insert(tk.END, "المصفوفة الأولية (Initial Matrix):\n", "arabic_step")
        self.print_matrix(text_area, matrix)
        
        if method == "gaussian":
            text_area.insert(tk.END, "\n--- Gaussian Elimination (REF) ---\n", "header")
            self.convert_to_ref(matrix, text_area)
            text_area.insert(tk.END, "\n--- Back Substitution ---\n", "header")
            self.back_substitution(matrix, text_area)
        else:
            text_area.insert(tk.END, "\n--- Forward Elimination ---\n", "header")
            self.convert_to_ref(matrix, text_area)
            text_area.insert(tk.END, "\n--- Gauss-Jordan (RREF) ---\n", "header")
            self.convert_to_rref(matrix, text_area)
            self.print_rref_solution(matrix, text_area)

    def print_matrix(self, text_widget, matrix):
        text_widget.insert(tk.END, "-" * 40 + "\n")
        rows = len(matrix)
        cols = len(matrix[0])
        for r in range(rows):
            line = "[ "
            for c in range(cols - 1):
                line += f"{str(matrix[r][c]):^8} "
            line += f"| {str(matrix[r][-1]):^8} ]\n"
            text_widget.insert(tk.END, line)
        text_widget.insert(tk.END, "-" * 40 + "\n\n")

    def convert_to_ref(self, matrix, text_widget):
        rows = len(matrix)
        cols = len(matrix[0]) - 1 
        pivot_row = 0
        for col in range(cols):
            if pivot_row >= rows: break
            
            # --- تعديل: عدم التبديل إلا إذا كان العنصر الحالي صفراً ---
            if matrix[pivot_row][col] == 0:
                # نبحث عن صف بديل تحته لا يساوي صفر
                swap_row = -1
                # نفضل اختيار أكبر قيمة لتجنب الكسور المعقدة إن أمكن، لكن الشرط الأساسي هو التبديل للضرورة
                candidates = [k for k in range(pivot_row + 1, rows) if matrix[k][col] != 0]
                
                if candidates:
                    # نختار الصف صاحب أكبر قيمة مطلقة من المرشحين (للحفاظ على دقة أفضل قليلاً حتى لو للضرورة)
                    max_row = candidates[0]
                    for k in candidates:
                        if abs(matrix[k][col]) > abs(matrix[max_row][col]):
                            max_row = k
                    
                    text_widget.insert(tk.END, f"تبديل الصف R{pivot_row+1} مع الصف R{max_row+1} (لأن العنصر المحوري صفر)\n", "arabic_step")
                    text_widget.insert(tk.END, f"Swap R{pivot_row+1} <-> R{max_row+1}\n")
                    matrix[pivot_row], matrix[max_row] = matrix[max_row], matrix[pivot_row]
                    self.print_matrix(text_widget, matrix)
                else:
                    # إذا كان العمود كله أصفار، ننتقل للعمود التالي
                    continue
            # --------------------------------------------------------

            step_performed = False
            for k in range(pivot_row + 1, rows):
                if matrix[k][col] == 0: continue
                
                factor = matrix[k][col] / matrix[pivot_row][col]
                if factor != 0:
                    if not step_performed:
                        text_widget.insert(tk.END, f"تصفير العناصر أسفل المحور في العمود {col+1}\n", "arabic_step")
                        step_performed = True
                    text_widget.insert(tk.END, f"R{k+1} = R{k+1} - ({factor}) * R{pivot_row+1}\n")
                    for j in range(col, cols + 1):
                        matrix[k][j] -= factor * matrix[pivot_row][j]
            
            if step_performed: self.print_matrix(text_widget, matrix)
            pivot_row += 1

    def back_substitution(self, matrix, text_widget):
        rows = len(matrix)
        cols = len(matrix[0]) - 1
        solution = [0] * cols
        
        # 1. Check Consistency (لا يوجد حل)
        for i in range(rows - 1, -1, -1):
            all_zeros = all(matrix[i][j] == 0 for j in range(cols))
            if all_zeros and matrix[i][cols] != 0:
                text_widget.insert(tk.END, "\nInconsistent System (No Solution)\n", "error")
                return

        # 2. Check Rank vs Variables (عدد لا نهائي)
        rank = 0
        for i in range(rows):
            if not all(matrix[i][j] == 0 for j in range(cols)):
                rank += 1
        
        if rank < cols:
            text_widget.insert(tk.END, f"\nRank ({rank}) < Variables ({cols})\n", "warning")
            text_widget.insert(tk.END, "Infinite Solutions\n", "final")
            return

        text_area = text_widget
        text_area.insert(tk.END, "حساب قيم المتغيرات بالتعويض من المعادلة الأخيرة للأولى\n", "arabic_step")
        try:
            for i in range(rank - 1, -1, -1):
                sum_val = sum(matrix[i][j] * solution[j] for j in range(i + 1, cols))
                solution[i] = (matrix[i][cols] - sum_val) / matrix[i][i]
                text_area.insert(tk.END, f"X{i+1} = {solution[i]}\n")

            text_area.insert(tk.END, "\nFinal Results:\n", "final")
            for i, val in enumerate(solution):
                text_area.insert(tk.END, f"X{i+1} = {val}\n", "final")
        except:
             text_area.insert(tk.END, "Infinite Solutions or Error\n", "final")

    def convert_to_rref(self, matrix, text_widget):
        rows = len(matrix)
        cols = len(matrix[0]) - 1
        for i in range(rows - 1, -1, -1):
            pivot_col = -1
            for j in range(cols):
                if matrix[i][j] != 0:
                    pivot_col = j
                    break
            if pivot_col == -1: continue

            pivot_val = matrix[i][pivot_col]
            if pivot_val != 1:
                text_widget.insert(tk.END, f"جعل العنصر المحوري 1 في الصف {i+1} (بالقسمة على {pivot_val})\n", "arabic_step")
                text_widget.insert(tk.END, f"R{i+1} = R{i+1} / {pivot_val}\n")
                for j in range(pivot_col, cols + 1):
                    matrix[i][j] /= pivot_val
                self.print_matrix(text_widget, matrix)

            step_performed = False
            for k in range(i - 1, -1, -1):
                factor = matrix[k][pivot_col]
                if factor != 0:
                    if not step_performed:
                        text_widget.insert(tk.END, f"تصفير القيم أعلى المحور في العمود {pivot_col+1}\n", "arabic_step")
                        step_performed = True
                    text_widget.insert(tk.END, f"R{k+1} = R{k+1} - ({factor}) * R{i+1}\n")
                    for j in range(pivot_col, cols + 1):
                        matrix[k][j] -= factor * matrix[i][j]
            if step_performed: self.print_matrix(text_widget, matrix)

    def print_rref_solution(self, matrix, text_widget):
        rows = len(matrix)
        cols = len(matrix[0]) - 1
        
        # 1. Check Consistency
        for i in range(rows):
            all_zeros = all(matrix[i][j] == 0 for j in range(cols))
            if all_zeros and matrix[i][cols] != 0:
                text_widget.insert(tk.END, "\nInconsistent System (No Solution)\n", "error")
                return

        # 2. Check Rank vs Variables
        pivot_count = 0
        solution_map = {}
        for i in range(rows):
            pivot_col = -1
            for j in range(cols):
                if matrix[i][j] != 0:
                    pivot_col = j
                    break
            if pivot_col != -1:
                pivot_count += 1
                solution_map[pivot_col] = matrix[i][cols]

        if pivot_count < cols:
            text_widget.insert(tk.END, f"\nRank ({pivot_count}) < Variables ({cols})\n", "warning")
            text_widget.insert(tk.END, "Infinite Solutions\n", "final")
            return

        text_widget.insert(tk.END, "Final Results:\n", "final")
        for j in range(cols):
            val = solution_map.get(j, "Free")
            text_widget.insert(tk.END, f"X{j+1} = {val}\n", "final")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedGaussSolver(root)
    root.mainloop()