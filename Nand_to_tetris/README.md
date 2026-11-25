# HACK COMPUTER LAB: MAKE THE COMPUTER DRAW A BOX
## ETCMTC301 Capstone Engineering Project
**Student Name:** Siya Singh  
**Roll Number:** 2501730417 (Roll Ending: 417)  
**Institution:** School of Engineering and Technology, K.R. Mangalam University  
**Evaluation Scope:** 10.0 / 10.0 Marks Scope  

---

### 🌐 Live Deployment
- **GitHub Repository:** [https://github.com/siya809026-dot/Nand2tetrisSiya2501730417](https://github.com/siya809026-dot/Nand2tetrisSiya2501730417)
- **Live GitHub Pages URL:** [https://siya809026-dot.github.io/Nand2tetrisSiya2501730417/](https://siya809026-dot.github.io/Nand2tetrisSiya2501730417/)
- **One-Click Deploy on Vercel:** [Deploy on Vercel](https://vercel.com/new/import?s=https%3A%2F%2Fgithub.com%2Fsiya809026-dot%2FNand2tetrisSiya2501730417)
- **One-Click Deploy on Render:** [Deploy on Render](https://render.com/deploy?repo=https://github.com/siya809026-dot/Nand2tetrisSiya2501730417)

---

### 📐 Project Architecture & Hardware Specifications
- **Parameter K:** 17 (derived from last digits of Roll Number `2501730417`)
- **Variant Rule ($K \pmod 3$):** `17 mod 3 = 2` &rarr; **Case 2: Duplicate Label Detection Warning**
- **Box Vertical Placement:** Starting Row 17, Height 20 rows (Row 17 to Row 36 inclusive)
- **Box Horizontal Placement:** Columns 0 to 31 (32 pixels wide = 2 16-bit words)
- **Screen Memory Mapping:**
  - Row 17 Word 0: `RAM[16384 + 17 * 32] = RAM[16928]`
  - Row 17 Word 1: `RAM[16929]`
  - Row 36 Word 0: `RAM[17536]`
  - Row 36 Word 1: `RAM[17537]`

---

### 📦 Deliverable Modules
1. **Part A: Hack Computer HDL (2.5 Marks)**
   - `CPU.hdl`, `Memory.hdl`, `Computer.hdl`, `ALU.hdl`
2. **Part B: Python Assembler & Symbol Table (3.0 Marks)**
   - `assembler.py` with pure two-pass resolution and K mod 3 = 2 diagnostic warnings
3. **Part C: Box Drawing Program & Emulator (2.5 Marks)**
   - `Box.asm`, `Box.hack`, `BoxTest.tst`, `BoxTest.cmp`
4. **Viva Voce Defense & Project Documentation (2.0 Marks)**
   - `PROJECT_REPORT.md`, `VIVA_PREPARATION.md`, `README.md`

---

### 🚀 Running Locally
```bash
# Option 1: Start local node server
npm start

# Visit in browser
http://localhost:3000/

# Option 2: Direct file
# Double click index.html in any browser (Chrome, Brave, Edge)
```
