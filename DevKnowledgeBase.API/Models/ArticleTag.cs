namespace DevKnowledgeBase.API.Models;

public class ArticleTag
{
    public Guid ArticleId { get; set; }
    public Guid TagId { get; set; }

    // Navigation properties
    public Article Article { get; set; } = null!;
    public Tag Tag { get; set; } = null!;
}
