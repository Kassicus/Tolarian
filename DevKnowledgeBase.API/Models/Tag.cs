namespace DevKnowledgeBase.API.Models;

public class Tag
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;

    // Navigation properties
    public ICollection<ArticleTag> ArticleTags { get; set; } = new List<ArticleTag>();
}
