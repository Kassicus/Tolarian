export interface Article {
  id: string;
  title: string;
  slug: string;
  content: string;
  categoryId?: string;
  categoryName?: string;
  createdAt: string;
  updatedAt: string;
  createdBy?: string;
  tags: Tag[];
}

export interface Tag {
  id: string;
  name: string;
  slug: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
}

export interface CreateArticleDto {
  title: string;
  content: string;
  categoryId?: string;
  createdBy?: string;
  tagIds: string[];
}

export interface UpdateArticleDto {
  title: string;
  content: string;
  categoryId?: string;
  tagIds: string[];
}
