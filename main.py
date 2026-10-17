import flet as ft
from datetime import datetime
import json
import os
def main(page:ft.Page):
    page.title="超市比价小助手"
    page.padding = 20
    page.appbar = ft.AppBar(
        title=ft.Text("🛒 抠门大法宝典", color="white", weight="bold"),
        bgcolor="green",
        center_title=True
    )
    page.scroll = ft.ScrollMode.AUTO

    storage_dir = os.getenv("FLET_APP_STORAGE_DATA", ".")
    json_path = os.path.join(storage_dir, "prices.json")
    if os.path.exists(json_path):
        with open(json_path,"r",encoding="utf-8") as f:
            try:
                price_data=json.load(f)
            except:
                price_data={}
    else:
        price_data={}
        
    item_input=ft.TextField(label="📦 商品名称",border_radius=10)
    store_select=ft.Dropdown(
        label="🏪选择超市",border_radius=10,
        options=[
            ft.dropdown.Option("99 Speedmart"),
            ft.dropdown.Option("C-Mart")
        ]
    )
    price_input=ft.TextField(label="💰 价格 (RM)", keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)

    status_text=ft.Text()

    result_list=ft.Column()
    def show_comparison(e=None):
        result_list.controls.clear()
        keyword=search_input.value.lower()

        def delete_item(item_to_delete):
            del price_data[item_to_delete]
            with open(json_path,"w",encoding="utf-8")as f:
                json.dump(price_data,f,ensure_ascii=False,indent=4)
            status_text.value=f"🗑️ 已删除：{item_to_delete}"
            show_comparison()

        for item_name,stores in price_data.items():
            if keyword not in item_name.lower():
                continue
            info_99=stores.get("99 Speedmart")
            info_cmart=stores.get("C-Mart")
            text_99=f"RM{info_99['price']}({info_99['date']})"if info_99 else"暂无记录"
            text_cmart=f"RM{info_cmart['price']}({info_cmart['date']})"if info_cmart else"暂无记录"

            if info_99 and info_cmart:
                p99=info_99["price"]
                pcm=info_cmart["price"]
                if p99<pcm:
                    advice=f"🏆 去 99 Speedmart 买！省 RM{round(pcm-p99,2)}"
                elif pcm<p99:
                    advice=f"🏆 去 C-Mart 买！省 RM{round(p99-pcm,2)}"  
                elif p99==pcm:
                    advice=f"🤝 两家价格一样！"
            else:
                advice="💡 还差一家超市的价格，下次去逛记得补上哦！"

            result_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=12,
                        content=ft.Row([
                            ft.Text(
                                f"🛒 【{item_name}】\n🏪 99: {text_99}\n🏬 C-Mart: {text_cmart}\n{advice}",
                                expand=True  # ✨ 让文字占满左边，自动换行不挤出屏幕！
                            ),
                            ft.Button(
                                content="🗑️",
                                on_click=lambda e, name=item_name: delete_item(name)
                            )
                        ])
                    )
                )
            )

            
        page.update()

    search_input=ft.TextField(label="🔍 搜索商品比价",on_change=show_comparison)

    def save_click(e):
        today=datetime.now().strftime("%Y-%m-%d")
        name=item_input.value
        store=store_select.value
        price=float(price_input.value)

        if name not in price_data:
            price_data[name]={}
        price_data[name][store]={"price":price,"date":today}

        with open(json_path,"w",encoding="utf-8")as f:
            json.dump(price_data,f,ensure_ascii=False,indent=4)

        status_text.value=f"✅ 已记录：[{today}]{item_input.value}在{store_select.value}卖 RM{price_input.value}"

        show_comparison()

        
    save_btn=ft.Button(content="保存价格",on_click=save_click)

    page.add(
        ft.SafeArea(
            ft.Column([
                item_input,
                store_select,
                price_input,
                save_btn,
                status_text,
                ft.Divider(),
                search_input,
                result_list
            ])
        )
    )

    show_comparison()
ft.run(main)
