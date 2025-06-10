def get_button_styles():
    """---CSS para os botões---"""
    return """
    <style>
        /* Versão Principal (ícone + texto) */
        .vm-main-btn-container {
            display: flex;
            gap: 16px;
            margin: 1.5rem 0;
        }
        .vm-main-btn {
            min-width: 160px;
            padding: 0.9rem 1.8rem;
            border-radius: 10px;
            font-weight: 600;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            border: none;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1;
        }
        .vm-main-btn::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                45deg,
                rgba(255,255,255,0.1),
                rgba(255,255,255,0.3),
                rgba(255,255,255,0.1)
            );
            transform: translateX(-100%);
            transition: transform 0.6s ease;
            z-index: -1;
        }
        .vm-main-btn:hover::before {
            transform: translateX(100%);
        }
        .vm-copy {
            background: linear-gradient(135deg, #8A2BE2 0%, #9d50bb 100%);
        }
        .vm-download {
            background: linear-gradient(135deg, #4776E6 0%, #8E54E9 100%);
        }
        .vm-main-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        .vm-main-btn:active {
            transform: translateY(0);
        }
        .vm-icon {
            margin-right: 10px;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }

        /* Versão Sidebar (apenas ícones) */
        .vm-sidebar-btns {
            display: flex;
            gap: 12px;
            margin-top: 10px;
            justify-content: center;
        }
        .vm-sidebar-btn {
            background: transparent;
            border: none;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            color: #ffffff;
            font-size: 18px;
            position: relative;
        }
        .vm-sidebar-btn:hover {
            background: rgba(110, 72, 170, 0.2);
            transform: scale(1.15);
        }
        .vm-sidebar-btn:active {
            transform: scale(0.95);
        }
        .vm-tooltip {
            position: absolute;
            bottom: -25px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(0,0,0,0.7);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            white-space: nowrap;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
        }
        .vm-sidebar-btn:hover .vm-tooltip {
            opacity: 1;
        }
        
    </style>
    """