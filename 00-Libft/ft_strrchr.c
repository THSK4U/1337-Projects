/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: tsellak <tsellak@student.1337.ma>          +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/18 23:42:47 by tsellak           #+#    #+#             */
/*   Updated: 2025/11/01 21:31:04 by tsellak          ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *s, int c)
{
	size_t	l_src;

	l_src = ft_strlen(s) + 1;
	while (l_src--)
	{
		if (s[l_src] == (char)c)
			return ((char *)s + l_src);
	}
	return (NULL);
}
