using System.Collections.ObjectModel;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace wk0105b;

/// <summary>
/// Interaction logic for MainWindow.xaml
/// </summary>
public partial class MainWindow : Window
{
// 資料繫結：WPF 會自動更新畫面
        public ObservableCollection<Book> Books { get; set; }

        public MainWindow()
        {
            InitializeComponent();
            
            Books = new ObservableCollection<Book>
            {
                new Book { Id = 1, Title = "C# 入門", IsBorrowed = false },
                new Book { Id = 2, Title = "設計模式", IsBorrowed = true },
                new Book { Id = 3, Title = "演算法導論", IsBorrowed = false }
            };

            // 將資料繫結到畫面上的 DataGrid
            BookDataGrid.ItemsSource = Books;
        }

        private void BorrowButton_Click(object sender, RoutedEventArgs e)
        {
            var selected = BookDataGrid.SelectedItem as Book;
            if (selected == null) 
            {
                MessageBox.Show("請先選擇一本書");
                return;
            }
            
            if (selected.IsBorrowed)
            {
                MessageBox.Show("這本書已被借出");
                return;
            }

            selected.IsBorrowed = true;
            // ObservableCollection 會自動通知畫面更新！
            MessageBox.Show("借書成功！");
        }
    }

    public class Book
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public bool IsBorrowed { get; set; }
    }

